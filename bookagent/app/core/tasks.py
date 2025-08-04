"""
异步任务管理模块
使用Celery处理长时间运行的任务
"""
import asyncio
from typing import Dict, Any, Optional
from celery import Celery
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# 创建Celery应用
celery_app = Celery(
    "bookagent",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.core.tasks"]
)

# Celery配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30分钟
    task_soft_time_limit=25 * 60,  # 25分钟
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

@celery_app.task(bind=True)
def generate_book_content_task(self, book_id: int, chapters: list):
    """异步生成图书内容任务"""
    try:
        # 更新任务状态
        self.update_state(
            state="PROGRESS",
            meta={"current": 0, "total": len(chapters), "status": "开始生成内容..."}
        )
        
        # 这里应该调用实际的内容生成逻辑
        # 由于是异步任务，需要使用同步版本的AI服务
        for i, chapter in enumerate(chapters):
            # 模拟内容生成
            logger.info(f"正在生成章节: {chapter['title']}")
            
            # 更新进度
            self.update_state(
                state="PROGRESS",
                meta={
                    "current": i + 1,
                    "total": len(chapters),
                    "status": f"正在生成章节: {chapter['title']}"
                }
            )
        
        return {
            "status": "SUCCESS",
            "message": "图书内容生成完成",
            "book_id": book_id
        }
        
    except Exception as exc:
        logger.error(f"图书内容生成失败: {exc}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(exc)}
        )
        raise

@celery_app.task(bind=True)
def export_book_task(self, book_id: int, format: str = "docx"):
    """异步导出图书任务"""
    try:
        self.update_state(
            state="PROGRESS",
            meta={"current": 0, "total": 100, "status": "开始导出图书..."}
        )
        
        # 模拟导出过程
        steps = [
            "准备数据...",
            "生成文档结构...",
            "应用样式...",
            "生成目录...",
            "保存文件..."
        ]
        
        for i, step in enumerate(steps):
            self.update_state(
                state="PROGRESS",
                meta={
                    "current": (i + 1) * 20,
                    "total": 100,
                    "status": step
                }
            )
        
        # 返回导出结果
        return {
            "status": "SUCCESS",
            "message": "图书导出完成",
            "book_id": book_id,
            "file_path": f"/exports/book_{book_id}.{format}"
        }
        
    except Exception as exc:
        logger.error(f"图书导出失败: {exc}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(exc)}
        )
        raise

class TaskManager:
    """任务管理器"""
    
    @staticmethod
    def start_book_generation(book_id: int, chapters: list) -> str:
        """启动图书生成任务"""
        task = generate_book_content_task.delay(book_id, chapters)
        return task.id
    
    @staticmethod
    def start_book_export(book_id: int, format: str = "docx") -> str:
        """启动图书导出任务"""
        task = export_book_task.delay(book_id, format)
        return task.id
    
    @staticmethod
    def get_task_status(task_id: str) -> Dict[str, Any]:
        """获取任务状态"""
        task = celery_app.AsyncResult(task_id)
        
        if task.state == "PENDING":
            return {
                "state": task.state,
                "status": "任务等待中..."
            }
        elif task.state == "PROGRESS":
            return {
                "state": task.state,
                "current": task.info.get("current", 0),
                "total": task.info.get("total", 1),
                "status": task.info.get("status", "")
            }
        elif task.state == "SUCCESS":
            return {
                "state": task.state,
                "result": task.info
            }
        else:  # FAILURE
            return {
                "state": task.state,
                "error": str(task.info)
            }
    
    @staticmethod
    def cancel_task(task_id: str) -> bool:
        """取消任务"""
        try:
            celery_app.control.revoke(task_id, terminate=True)
            return True
        except Exception as e:
            logger.error(f"取消任务失败: {e}")
            return False

# 全局任务管理器实例
task_manager = TaskManager()