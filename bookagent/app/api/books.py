"""
图书相关API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..core import security
from ..core.database import get_db
from ..models.book import Book
from ..models.user import User
from ..schemas.book import Book as BookSchema, BookCreate, BookUpdate, BookInDB

router = APIRouter()

def get_books(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    user_id: Optional[int] = None
):
    """获取图书列表"""
    query = db.query(Book)
    if user_id is not None:
        query = query.filter(Book.author_id == user_id)
    return query.offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    """获取单个图书"""
    return db.query(Book).filter(Book.id == book_id).first()

def create_book(db: Session, book: BookCreate, author_id: int):
    """创建图书"""
    db_book = Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: BookUpdate):
    """更新图书"""
    db_book = get_book(db, book_id=book_id)
    if not db_book:
        return None
    
    update_data = book.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    """删除图书"""
    db_book = get_book(db, book_id=book_id)
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book

@router.post("/books/", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
def create_book_endpoint(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_user)
):
    """创建新图书"""
    return create_book(db=db, book=book, author_id=current_user.id)

@router.get("/books/", response_model=List[BookSchema])
def read_books(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_user)
):
    """获取图书列表"""
    # 非管理员只能查看自己的书
    if not current_user.is_superuser and user_id != current_user.id:
        user_id = current_user.id
    
    books = get_books(db, skip=skip, limit=limit, user_id=user_id)
    return books

@router.get("/books/{book_id}", response_model=BookSchema)
def read_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_user)
):
    """获取指定图书"""
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="图书不存在")
    
    # 检查权限
    if db_book.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限访问此资源"
        )
    
    return db_book

@router.put("/books/{book_id}", response_model=BookSchema)
def update_book_endpoint(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_user)
):
    """更新图书信息"""
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="图书不存在")
    
    # 检查权限
    if db_book.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限修改此资源"
        )
    
    return update_book(db=db, book_id=book_id, book=book)

@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_endpoint(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_user)
):
    """删除图书"""
    db_book = get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="图书不存在")
    
    # 检查权限
    if db_book.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除此资源"
        )
    
    delete_book(db=db, book_id=book_id)
    return {"ok": True}
