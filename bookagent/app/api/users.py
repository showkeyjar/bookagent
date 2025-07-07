"""
用户相关API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core import security
from ..core.database import get_db
from ..models.user import User
from ..schemas.user import User as UserSchema, UserCreate, UserUpdate

router = APIRouter()

def get_user(db: Session, user_id: int):
    """获取单个用户"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """根据用户名获取用户"""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """根据邮箱获取用户"""
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """获取用户列表"""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    """创建用户"""
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_superuser=user.is_superuser
    )
    db_user.set_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    """更新用户"""
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        return None
    
    update_data = user.dict(exclude_unset=True)
    if "password" in update_data:
        hashed_password = security.get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """删除用户"""
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

@router.post("/users/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_superuser)
):
    """创建新用户（管理员）"""
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="用户名已存在"
        )
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="邮箱已存在"
        )
    return create_user(db=db, user=user)

@router.get("/users/", response_model=List[UserSchema])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_superuser)
):
    """获取用户列表（管理员）"""
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(security.get_current_active_user)
):
    """获取当前用户信息"""
    return current_user

@router.get("/users/{user_id}", response_model=UserSchema)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_superuser)
):
    """获取指定用户信息（管理员）"""
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

@router.put("/users/me", response_model=UserSchema)
def update_user_me(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_user)
):
    """更新当前用户信息"""
    return update_user(db=db, user_id=current_user.id, user=user)

@router.put("/users/{user_id}", response_model=UserSchema)
def update_user_endpoint(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_superuser)
):
    """更新指定用户信息（管理员）"""
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return update_user(db=db, user_id=user_id, user=user)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_superuser)
):
    """删除用户（管理员）"""
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    delete_user(db=db, user_id=user_id)
    return {"ok": True}
