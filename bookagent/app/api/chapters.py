"""
章节相关API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core import security
from ..core.database import get_db
from ..models.chapter import Chapter
from ..models.book import Book
from ..models.user import User
from ..schemas.chapter import Chapter as ChapterSchema, ChapterCreate, ChapterUpdate

router = APIRouter()

def get_chapters(
    db: Session, 
    book_id: int,
    skip: int = 0, 
    limit: int = 100
):
    """获取章节列表"""
    return (
        db.query(Chapter)
        .filter(Chapter.book_id == book_id)
        .order_by(Chapter.order)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_chapter(db: Session, chapter_id: int):
    """获取单个章节"""
    return db.query(Chapter).filter(Chapter.id == chapter_id).first()

def create_chapter(db: Session, chapter: ChapterCreate, book_id: int, author_id: int):
    """创建章节"""
    # 验证图书存在且属于当前用户
    book = db.query(Book).filter(Book.id == book_id, Book.author_id == author_id).first()
    if not book:
        return None
    
    db_chapter = Chapter(**chapter.dict(), book_id=book_id)
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter

def update_chapter(db: Session, chapter_id: int, chapter: ChapterUpdate):
    """更新章节"""
    db_chapter = get_chapter(db, chapter_id=chapter_id)
    if not db_chapter:
        return None
    
    update_data = chapter.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_chapter, field, value)
    
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter

def delete_chapter(db: Session, chapter_id: int):
    """删除章节"""
    db_chapter = get_chapter(db, chapter_id=chapter_id)
    if not db_chapter:
        return None
    db.delete(db_chapter)
    db.commit()
    return db_chapter

def check_book_ownership(db: Session, book_id: int, user_id: int):
    """检查用户是否有权限操作该图书"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="图书不存在")
    if book.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限操作此资源"
        )
    return book

@router.post("/books/{book_id}/chapters/", response_model=ChapterSchema, status_code=status.HTTP_201_CREATED)
def create_chapter_endpoint(
    book_id: int,
    chapter: ChapterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_user)
):
    """创建新章节"""
    check_book_ownership(db, book_id, current_user.id)
    db_chapter = create_chapter(
        db=db, 
        chapter=chapter, 
        book_id=book_id,
        author_id=current_user.id
    )
    if db_chapter is None:
        raise HTTPException(status_code=400, detail="创建章节失败")
    return db_chapter

@router.get("/books/{book_id}/chapters/", response_model=List[ChapterSchema])
def read_chapters(
    book_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_user)
):
    """获取章节列表"""
    check_book_ownership(db, book_id, current_user.id)
    chapters = get_chapters(db, book_id=book_id, skip=skip, limit=limit)
    return chapters

@router.get("/chapters/{chapter_id}", response_model=ChapterSchema)
def read_chapter(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_user)
):
    """获取指定章节"""
    db_chapter = get_chapter(db, chapter_id=chapter_id)
    if db_chapter is None:
        raise HTTPException(status_code=404, detail="章节不存在")
    
    # 检查权限
    book = db.query(Book).filter(Book.id == db_chapter.book_id).first()
    if book.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限访问此资源"
        )
    
    return db_chapter

@router.put("/chapters/{chapter_id}", response_model=ChapterSchema)
def update_chapter_endpoint(
    chapter_id: int,
    chapter: ChapterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_user)
):
    """更新章节信息"""
    db_chapter = get_chapter(db, chapter_id=chapter_id)
    if db_chapter is None:
        raise HTTPException(status_code=404, detail="章节不存在")
    
    # 检查权限
    book = db.query(Book).filter(Book.id == db_chapter.book_id).first()
    if book.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限修改此资源"
        )
    
    return update_chapter(db=db, chapter_id=chapter_id, chapter=chapter)

@router.delete("/chapters/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chapter_endpoint(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_active_user)
):
    """删除章节"""
    db_chapter = get_chapter(db, chapter_id=chapter_id)
    if db_chapter is None:
        raise HTTPException(status_code=404, detail="章节不存在")
    
    # 检查权限
    book = db.query(Book).filter(Book.id == db_chapter.book_id).first()
    if book.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除此资源"
        )
    
    delete_chapter(db=db, chapter_id=chapter_id)
    return {"ok": True}
