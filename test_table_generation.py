#!/usr/bin/env python3
"""
测试表格生成功能
"""
import asyncio
from bookagent.app.services.ai_service import get_ai_service


async def test_table_generation():
    """测试表格生成功能"""
    # 获取AI服务实例
    ai_service = await get_ai_service()

    # 测试场景1: 生成包含对比信息的章节，应该自动生成表格
    print("测试场景1: 生成包含对比信息的章节")
    title1 = "不同编程语言特性对比"
    content1 = await ai_service.generate_chapter_content(
        title=title1,
        style="technical",
        language="zh",
        length="medium",
        use_tables=True
    )
    print(f"\n生成的内容:\n{content1}")
    print(f"\n是否包含表格: {'是' if '|' in content1 and '-' in content1 else '否'}")

    # 测试场景2: 禁用表格生成功能
    print("\n测试场景2: 禁用表格生成功能")
    title2 = "编程范式介绍"
    content2 = await ai_service.generate_chapter_content(
        title=title2,
        style="technical",
        language="zh",
        length="medium",
        use_tables=False
    )
    print(f"\n生成的内容:\n{content2}")
    print(f"\n是否包含表格: {'是' if '|' in content2 and '-' in content2 else '否'}")


if __name__ == '__main__':
    # 运行测试
    asyncio.run(test_table_generation())