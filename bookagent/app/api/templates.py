"""
模板相关API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core import security
from ..core.database import get_db
from ..models.template import Template
from ..models.user import User
from ..schemas.template import Template as TemplateSchema, TemplateCreate, TemplateUpdate

router = APIRouter()

def get_templates(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    template_type: Optional[str] = None,
    is_default: Optional[bool] = None
):
    """获取模板列表"""
    query = db.query(Template)
    
    if template_type:
        query = query.filter(Template.template_type == template_type)
    if is_default is not None:
        query = query.filter(Template.is_default == is_default)
    
    return query.offset(skip).limit(limit).all()

def get_template(db: Session, template_id: int):
    """获取单个模板"""
    return db.query(Template).filter(Template.id == template_id).first()

def create_template(db: Session, template: TemplateCreate, author_id: Optional[int] = None):
    """创建模板"""
    # 如果设置为默认模板，则取消其他同类型模板的默认状态
    if template.is_default:
        db.query(Template).filter(
            Template.template_type == template.template_type,
            Template.is_default == True
        ).update({"is_default": False})
    
    db_template = Template(**template.dict(), author_id=author_id)
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

def update_template(db: Session, template_id: int, template: TemplateUpdate):
    """更新模板"""
    db_template = get_template(db, template_id=template_id)
    if not db_template:
        return None
    
    update_data = template.dict(exclude_unset=True)
    
    # 如果更新为默认模板，则取消其他同类型模板的默认状态
    if update_data.get('is_default', False):
        db.query(Template).filter(
            Template.template_type == (update_data.get('template_type') or db_template.template_type),
            Template.is_default == True,
            Template.id != template_id
        ).update({"is_default": False})
    
    for field, value in update_data.items():
        setattr(db_template, field, value)
    
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

def delete_template(db: Session, template_id: int):
    """删除模板"""
    db_template = get_template(db, template_id=template_id)
    if not db_template:
        return None
    
    # 检查是否有章节在使用此模板
    from ..models.chapter import Chapter
    chapter_count = db.query(Chapter).filter(Chapter.template_id == template_id).count()
    if chapter_count > 0:
        return "in_use"
    
    db.delete(db_template)
    db.commit()
    return db_template

@router.post("/", response_model=TemplateSchema, status_code=status.HTTP_201_CREATED)
def create_template_endpoint(
    template: TemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_user)
):
    """创建新模板"""
    db_template = create_template(
        db=db, 
        template=template,
        author_id=current_user.id
    )
    if db_template is None:
        raise HTTPException(status_code=400, detail="创建模板失败")
    return db_template

@router.get("/", response_model=List[TemplateSchema])
def read_templates(
    template_type: Optional[str] = None,
    is_default: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取模板列表"""
    templates = get_templates(
        db, 
        template_type=template_type,
        is_default=is_default,
        skip=skip, 
        limit=limit
    )
    return templates

@router.get("/{template_id}", response_model=TemplateSchema)
def read_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_user)
):
    """获取指定模板"""
    db_template = get_template(db, template_id=template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="模板不存在")
    return db_template

@router.put("/{template_id}", response_model=TemplateSchema)
def update_template_endpoint(
    template_id: int,
    template: TemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_superuser)
):
    """更新模板信息（管理员）"""
    db_template = update_template(db=db, template_id=template_id, template=template)
    if db_template is None:
        raise HTTPException(status_code=404, detail="模板不存在")
    return db_template

@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template_endpoint(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_superuser)
):
    """删除模板（管理员）"""
    result = delete_template(db=db, template_id=template_id)
    if result is None:
        raise HTTPException(status_code=404, detail="模板不存在")
    if result == "in_use":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法删除正在使用的模板"
        )
    return {"ok": True}
