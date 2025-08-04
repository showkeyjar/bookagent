"""
图表生成服务
支持生成各种技术图表，包括架构图、流程图、时序图等
"""
import os
import io
import base64
import tempfile
import logging
from typing import Dict, Any, Optional, List, Union, Tuple
from pathlib import Path
import json

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import graphviz
from PIL import Image, ImageDraw, ImageFont
import cairosvg

from ..core.config import settings

logger = logging.getLogger(__name__)

class DiagramType:
    """图表类型常量"""
    ARCHITECTURE = "architecture"
    FLOWCHART = "flowchart"
    SEQUENCE = "sequence"
    CLASS_DIAGRAM = "class_diagram"
    NETWORK = "network"
    TIMELINE = "timeline"
    MINDMAP = "mindmap"
    SYSTEM_DESIGN = "system_design"

class DiagramService:
    """图表生成服务"""
    
    def __init__(self):
        self.output_dir = Path(settings.MEDIA_ROOT) / "diagrams"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 设置中文字体支持
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
    
    async def generate_diagram(
        self,
        diagram_type: str,
        content: Dict[str, Any],
        title: str = "",
        style: str = "modern",
        format: str = "png",
        **kwargs
    ) -> Dict[str, Any]:
        """
        生成图表
        
        Args:
            diagram_type: 图表类型
            content: 图表内容数据
            title: 图表标题
            style: 图表样式
            format: 输出格式 (png, svg, pdf)
            **kwargs: 其他参数
            
        Returns:
            包含图表信息的字典
        """
        try:
            if diagram_type == DiagramType.ARCHITECTURE:
                return await self._generate_architecture_diagram(content, title, style, format, **kwargs)
            elif diagram_type == DiagramType.FLOWCHART:
                return await self._generate_flowchart(content, title, style, format, **kwargs)
            elif diagram_type == DiagramType.SEQUENCE:
                return await self._generate_sequence_diagram(content, title, style, format, **kwargs)
            elif diagram_type == DiagramType.CLASS_DIAGRAM:
                return await self._generate_class_diagram(content, title, style, format, **kwargs)
            elif diagram_type == DiagramType.NETWORK:
                return await self._generate_network_diagram(content, title, style, format, **kwargs)
            elif diagram_type == DiagramType.TIMELINE:
                return await self._generate_timeline(content, title, style, format, **kwargs)
            elif diagram_type == DiagramType.MINDMAP:
                return await self._generate_mindmap(content, title, style, format, **kwargs)
            elif diagram_type == DiagramType.SYSTEM_DESIGN:
                return await self._generate_system_design(content, title, style, format, **kwargs)
            else:
                raise ValueError(f"不支持的图表类型: {diagram_type}")
                
        except Exception as e:
            logger.error(f"生成图表失败: {str(e)}", exc_info=True)
            raise
    
    async def _generate_architecture_diagram(
        self,
        content: Dict[str, Any],
        title: str,
        style: str,
        format: str,
        **kwargs
    ) -> Dict[str, Any]:
        """生成架构图"""
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.axis('off')
        
        # 设置颜色主题
        colors = self._get_color_theme(style)
        
        # 绘制标题
        if title:
            ax.text(5, 7.5, title, fontsize=16, fontweight='bold', ha='center')
        
        # 解析架构组件
        components = content.get('components', [])
        connections = content.get('connections', [])
        layers = content.get('layers', [])
        
        # 绘制层级
        layer_height = 1.5
        for i, layer in enumerate(layers):
            y_pos = 6 - i * layer_height
            # 绘制层级背景
            rect = FancyBboxPatch(
                (0.5, y_pos - 0.6), 9, 1.2,
                boxstyle="round,pad=0.1",
                facecolor=colors['layer_bg'],
                edgecolor=colors['layer_border'],
                alpha=0.3
            )
            ax.add_patch(rect)
            
            # 层级标题
            ax.text(0.2, y_pos, layer.get('name', ''), fontsize=12, fontweight='bold', va='center')
            
            # 绘制层级中的组件
            layer_components = layer.get('components', [])
            comp_width = 8 / max(len(layer_components), 1)
            for j, comp in enumerate(layer_components):
                x_pos = 1 + j * comp_width + comp_width/2
                
                # 组件框
                comp_rect = FancyBboxPatch(
                    (x_pos - comp_width/3, y_pos - 0.3), comp_width*2/3, 0.6,
                    boxstyle="round,pad=0.05",
                    facecolor=colors['component_bg'],
                    edgecolor=colors['component_border']
                )
                ax.add_patch(comp_rect)
                
                # 组件名称
                ax.text(x_pos, y_pos, comp.get('name', ''), fontsize=10, ha='center', va='center')
        
        # 绘制连接线
        for conn in connections:
            start = conn.get('start', {})
            end = conn.get('end', {})
            if start and end:
                ax.annotate('', xy=(end.get('x', 0), end.get('y', 0)), 
                           xytext=(start.get('x', 0), start.get('y', 0)),
                           arrowprops=dict(arrowstyle='->', color=colors['arrow'], lw=2))
        
        # 保存图表
        return await self._save_diagram(fig, title or "architecture", format)
    
    async def _generate_flowchart(
        self,
        content: Dict[str, Any],
        title: str,
        style: str,
        format: str,
        **kwargs
    ) -> Dict[str, Any]:
        """生成流程图"""
        # 使用Graphviz生成流程图
        dot = graphviz.Digraph(comment=title)
        dot.attr(rankdir='TB', size='10,8')
        dot.attr('node', shape='box', style='rounded,filled', fontname='SimHei')
        
        # 设置样式
        colors = self._get_color_theme(style)
        
        # 添加节点
        nodes = content.get('nodes', [])
        for node in nodes:
            node_id = node.get('id', '')
            node_label = node.get('label', '')
            node_type = node.get('type', 'process')
            
            # 根据节点类型设置样式
            if node_type == 'start':
                dot.node(node_id, node_label, shape='ellipse', fillcolor=colors['start_node'])
            elif node_type == 'end':
                dot.node(node_id, node_label, shape='ellipse', fillcolor=colors['end_node'])
            elif node_type == 'decision':
                dot.node(node_id, node_label, shape='diamond', fillcolor=colors['decision_node'])
            else:
                dot.node(node_id, node_label, fillcolor=colors['process_node'])
        
        # 添加边
        edges = content.get('edges', [])
        for edge in edges:
            from_node = edge.get('from', '')
            to_node = edge.get('to', '')
            label = edge.get('label', '')
            
            if from_node and to_node:
                dot.edge(from_node, to_node, label=label)
        
        # 渲染图表
        output_path = self.output_dir / f"{title or 'flowchart'}_{hash(str(content))}"
        dot.render(str(output_path), format=format, cleanup=True)
        
        return {
            'success': True,
            'file_path': f"{output_path}.{format}",
            'diagram_type': DiagramType.FLOWCHART,
            'title': title
        }
    
    async def _generate_sequence_diagram(
        self,
        content: Dict[str, Any],
        title: str,
        style: str,
        format: str,
        **kwargs
    ) -> Dict[str, Any]:
        """生成时序图"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 获取参与者和消息
        participants = content.get('participants', [])
        messages = content.get('messages', [])
        
        if not participants:
            raise ValueError("时序图必须包含参与者")
        
        # 设置颜色主题
        colors = self._get_color_theme(style)
        
        # 计算布局
        num_participants = len(participants)
        x_positions = {p['id']: i * (10 / (num_participants - 1)) for i, p in enumerate(participants)}
        
        # 绘制参与者
        for i, participant in enumerate(participants):
            x = x_positions[participant['id']]
            # 参与者框
            rect = FancyBboxPatch(
                (x - 0.8, 7), 1.6, 0.8,
                boxstyle="round,pad=0.1",
                facecolor=colors['participant_bg'],
                edgecolor=colors['participant_border']
            )
            ax.add_patch(rect)
            ax.text(x, 7.4, participant['name'], ha='center', va='center', fontweight='bold')
            
            # 生命线
            ax.plot([x, x], [7, 0.5], color=colors['lifeline'], linestyle='--', alpha=0.7)
        
        # 绘制消息
        y_pos = 6.5
        for message in messages:
            from_id = message.get('from')
            to_id = message.get('to')
            text = message.get('text', '')
            msg_type = message.get('type', 'sync')
            
            if from_id in x_positions and to_id in x_positions:
                x1 = x_positions[from_id]
                x2 = x_positions[to_id]
                
                # 消息箭头
                arrow_style = '->' if msg_type == 'sync' else '-->'
                ax.annotate('', xy=(x2, y_pos), xytext=(x1, y_pos),
                           arrowprops=dict(arrowstyle=arrow_style, color=colors['message_arrow']))
                
                # 消息文本
                mid_x = (x1 + x2) / 2
                ax.text(mid_x, y_pos + 0.1, text, ha='center', va='bottom', fontsize=9)
                
                y_pos -= 0.4
        
        # 设置图表属性
        ax.set_xlim(-1, 11)
        ax.set_ylim(0, 8)
        ax.axis('off')
        
        if title:
            ax.text(5, 7.8, title, fontsize=14, fontweight='bold', ha='center')
        
        return await self._save_diagram(fig, title or "sequence", format)
    
    async def _generate_class_diagram(
        self,
        content: Dict[str, Any],
        title: str,
        style: str,
        format: str,
        **kwargs
    ) -> Dict[str, Any]:
        """生成类图"""
        dot = graphviz.Digraph(comment=title)
        dot.attr(rankdir='TB', size='12,10')
        dot.attr('node', shape='record', style='filled', fontname='SimHei')
        
        colors = self._get_color_theme(style)
        
        # 添加类
        classes = content.get('classes', [])
        for cls in classes:
            class_id = cls.get('id', '')
            class_name = cls.get('name', '')
            attributes = cls.get('attributes', [])
            methods = cls.get('methods', [])
            
            # 构建类的标签
            label_parts = [f"{{<class>{class_name}}}"]
            
            if attributes:
                attr_str = "\\l".join([f"- {attr}" for attr in attributes])
                label_parts.append(f"{{{attr_str}\\l}}")
            
            if methods:
                method_str = "\\l".join([f"+ {method}" for method in methods])
                label_parts.append(f"{{{method_str}\\l}}")
            
            label = "|".join(label_parts)
            dot.node(class_id, label, fillcolor=colors['class_bg'])
        
        # 添加关系
        relationships = content.get('relationships', [])
        for rel in relationships:
            from_class = rel.get('from', '')
            to_class = rel.get('to', '')
            rel_type = rel.get('type', 'association')
            
            if from_class and to_class:
                if rel_type == 'inheritance':
                    dot.edge(from_class, to_class, arrowhead='empty')
                elif rel_type == 'composition':
                    dot.edge(from_class, to_class, arrowhead='diamond')
                else:
                    dot.edge(from_class, to_class)
        
        # 渲染图表
        output_path = self.output_dir / f"{title or 'class_diagram'}_{hash(str(content))}"
        dot.render(str(output_path), format=format, cleanup=True)
        
        return {
            'success': True,
            'file_path': f"{output_path}.{format}",
            'diagram_type': DiagramType.CLASS_DIAGRAM,
            'title': title
        }
    
    async def _generate_network_diagram(
        self,
        content: Dict[str, Any],
        title: str,
        style: str,
        format: str,
        **kwargs
    ) -> Dict[str, Any]:
        """生成网络拓扑图"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        nodes = content.get('nodes', [])
        edges = content.get('edges', [])
        
        colors = self._get_color_theme(style)
        
        # 简单的圆形布局
        import math
        num_nodes = len(nodes)
        node_positions = {}
        
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / num_nodes
            x = 5 + 3 * math.cos(angle)
            y = 4 + 3 * math.sin(angle)
            node_positions[node['id']] = (x, y)
            
            # 绘制节点
            node_type = node.get('type', 'server')
            if node_type == 'server':
                color = colors['server_node']
            elif node_type == 'client':
                color = colors['client_node']
            else:
                color = colors['default_node']
            
            circle = plt.Circle((x, y), 0.5, color=color, alpha=0.8)
            ax.add_patch(circle)
            ax.text(x, y, node.get('name', ''), ha='center', va='center', fontweight='bold')
        
        # 绘制连接
        for edge in edges:
            from_id = edge.get('from')
            to_id = edge.get('to')
            
            if from_id in node_positions and to_id in node_positions:
                x1, y1 = node_positions[from_id]
                x2, y2 = node_positions[to_id]
                ax.plot([x1, x2], [y1, y2], color=colors['connection'], linewidth=2, alpha=0.7)
        
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.axis('off')
        
        if title:
            ax.text(5, 7.5, title, fontsize=14, fontweight='bold', ha='center')
        
        return await self._save_diagram(fig, title or "network", format)
    
    async def _generate_timeline(
        self,
        content: Dict[str, Any],
        title: str,
        style: str,
        format: str,
        **kwargs
    ) -> Dict[str, Any]:
        """生成时间线图"""
        fig, ax = plt.subplots(figsize=(14, 6))
        
        events = content.get('events', [])
        colors = self._get_color_theme(style)
        
        # 绘制时间线主轴
        ax.axhline(y=0, color=colors['timeline_axis'], linewidth=3)
        
        # 绘制事件
        for i, event in enumerate(events):
            x_pos = i * 2
            y_pos = 0.5 if i % 2 == 0 else -0.5
            
            # 事件点
            ax.scatter(x_pos, 0, s=100, color=colors['event_point'], zorder=3)
            
            # 连接线
            ax.plot([x_pos, x_pos], [0, y_pos], color=colors['event_line'], linewidth=2)
            
            # 事件框
            bbox_props = dict(boxstyle="round,pad=0.3", facecolor=colors['event_bg'], alpha=0.8)
            ax.text(x_pos, y_pos, event.get('title', ''), ha='center', va='center',
                   bbox=bbox_props, fontweight='bold')
            
            # 时间标签
            ax.text(x_pos, -0.8 if y_pos > 0 else 0.8, event.get('date', ''), 
                   ha='center', va='center', fontsize=9, style='italic')
        
        ax.set_xlim(-1, len(events) * 2)
        ax.set_ylim(-2, 2)
        ax.axis('off')
        
        if title:
            ax.text(len(events), 1.5, title, fontsize=14, fontweight='bold', ha='center')
        
        return await self._save_diagram(fig, title or "timeline", format)
    
    async def _generate_mindmap(
        self,
        content: Dict[str, Any],
        title: str,
        style: str,
        format: str,
        **kwargs
    ) -> Dict[str, Any]:
        """生成思维导图"""
        fig, ax = plt.subplots(figsize=(12, 10))
        
        root = content.get('root', {})
        branches = content.get('branches', [])
        colors = self._get_color_theme(style)
        
        # 绘制中心节点
        center_x, center_y = 6, 5
        center_circle = plt.Circle((center_x, center_y), 1, color=colors['mindmap_center'], alpha=0.8)
        ax.add_patch(center_circle)
        ax.text(center_x, center_y, root.get('text', ''), ha='center', va='center', 
               fontweight='bold', fontsize=12)
        
        # 绘制分支
        import math
        num_branches = len(branches)
        for i, branch in enumerate(branches):
            angle = 2 * math.pi * i / num_branches
            branch_x = center_x + 3 * math.cos(angle)
            branch_y = center_y + 3 * math.sin(angle)
            
            # 分支连接线
            ax.plot([center_x, branch_x], [center_y, branch_y], 
                   color=colors['mindmap_branch'], linewidth=3, alpha=0.7)
            
            # 分支节点
            branch_circle = plt.Circle((branch_x, branch_y), 0.6, 
                                     color=colors['mindmap_node'], alpha=0.8)
            ax.add_patch(branch_circle)
            ax.text(branch_x, branch_y, branch.get('text', ''), ha='center', va='center',
                   fontweight='bold', fontsize=10)
            
            # 子分支
            sub_branches = branch.get('children', [])
            for j, sub_branch in enumerate(sub_branches):
                sub_angle = angle + (j - len(sub_branches)/2) * 0.3
                sub_x = branch_x + 1.5 * math.cos(sub_angle)
                sub_y = branch_y + 1.5 * math.sin(sub_angle)
                
                ax.plot([branch_x, sub_x], [branch_y, sub_y], 
                       color=colors['mindmap_sub_branch'], linewidth=2, alpha=0.6)
                
                ax.text(sub_x, sub_y, sub_branch.get('text', ''), ha='center', va='center',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor=colors['mindmap_sub_node'], alpha=0.7),
                       fontsize=8)
        
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        if title:
            ax.text(6, 9, title, fontsize=14, fontweight='bold', ha='center')
        
        return await self._save_diagram(fig, title or "mindmap", format)
    
    async def _generate_system_design(
        self,
        content: Dict[str, Any],
        title: str,
        style: str,
        format: str,
        **kwargs
    ) -> Dict[str, Any]:
        """生成系统设计图"""
        fig, ax = plt.subplots(figsize=(16, 12))
        
        components = content.get('components', [])
        connections = content.get('connections', [])
        colors = self._get_color_theme(style)
        
        # 绘制组件
        for comp in components:
            x = comp.get('x', 0)
            y = comp.get('y', 0)
            width = comp.get('width', 2)
            height = comp.get('height', 1)
            comp_type = comp.get('type', 'service')
            
            # 根据组件类型选择颜色
            if comp_type == 'database':
                color = colors['database_comp']
            elif comp_type == 'cache':
                color = colors['cache_comp']
            elif comp_type == 'queue':
                color = colors['queue_comp']
            elif comp_type == 'api':
                color = colors['api_comp']
            else:
                color = colors['service_comp']
            
            # 绘制组件框
            rect = FancyBboxPatch(
                (x, y), width, height,
                boxstyle="round,pad=0.1",
                facecolor=color,
                edgecolor=colors['component_border'],
                linewidth=2
            )
            ax.add_patch(rect)
            
            # 组件标签
            ax.text(x + width/2, y + height/2, comp.get('name', ''), 
                   ha='center', va='center', fontweight='bold', fontsize=10)
        
        # 绘制连接
        for conn in connections:
            from_comp = conn.get('from', {})
            to_comp = conn.get('to', {})
            conn_type = conn.get('type', 'sync')
            
            if from_comp and to_comp:
                x1 = from_comp.get('x', 0) + from_comp.get('width', 2) / 2
                y1 = from_comp.get('y', 0) + from_comp.get('height', 1) / 2
                x2 = to_comp.get('x', 0) + to_comp.get('width', 2) / 2
                y2 = to_comp.get('y', 0) + to_comp.get('height', 1) / 2
                
                # 连接线样式
                if conn_type == 'async':
                    linestyle = '--'
                else:
                    linestyle = '-'
                
                ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                           arrowprops=dict(arrowstyle='->', color=colors['connection_arrow'], 
                                         linestyle=linestyle, linewidth=2))
                
                # 连接标签
                if conn.get('label'):
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    ax.text(mid_x, mid_y, conn['label'], ha='center', va='center',
                           bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8),
                           fontsize=8)
        
        ax.set_xlim(-1, 15)
        ax.set_ylim(-1, 11)
        ax.axis('off')
        
        if title:
            ax.text(7, 10.5, title, fontsize=16, fontweight='bold', ha='center')
        
        return await self._save_diagram(fig, title or "system_design", format)
    
    def _get_color_theme(self, style: str) -> Dict[str, str]:
        """获取颜色主题"""
        themes = {
            'modern': {
                'layer_bg': '#E3F2FD',
                'layer_border': '#1976D2',
                'component_bg': '#FFFFFF',
                'component_border': '#424242',
                'arrow': '#1976D2',
                'start_node': '#4CAF50',
                'end_node': '#F44336',
                'decision_node': '#FF9800',
                'process_node': '#2196F3',
                'participant_bg': '#E1F5FE',
                'participant_border': '#0277BD',
                'lifeline': '#757575',
                'message_arrow': '#1976D2',
                'class_bg': '#F3E5F5',
                'server_node': '#4CAF50',
                'client_node': '#2196F3',
                'default_node': '#9E9E9E',
                'connection': '#757575',
                'timeline_axis': '#424242',
                'event_point': '#1976D2',
                'event_line': '#757575',
                'event_bg': '#E3F2FD',
                'mindmap_center': '#1976D2',
                'mindmap_branch': '#757575',
                'mindmap_node': '#4CAF50',
                'mindmap_sub_branch': '#BDBDBD',
                'mindmap_sub_node': '#E8F5E8',
                'database_comp': '#FF9800',
                'cache_comp': '#E91E63',
                'queue_comp': '#9C27B0',
                'api_comp': '#2196F3',
                'service_comp': '#4CAF50',
                'connection_arrow': '#424242'
            },
            'classic': {
                'layer_bg': '#F5F5F5',
                'layer_border': '#333333',
                'component_bg': '#FFFFFF',
                'component_border': '#000000',
                'arrow': '#000000',
                'start_node': '#90EE90',
                'end_node': '#FFB6C1',
                'decision_node': '#FFD700',
                'process_node': '#87CEEB',
                'participant_bg': '#F0F8FF',
                'participant_border': '#000080',
                'lifeline': '#696969',
                'message_arrow': '#000080',
                'class_bg': '#FFFACD',
                'server_node': '#90EE90',
                'client_node': '#87CEEB',
                'default_node': '#D3D3D3',
                'connection': '#696969',
                'timeline_axis': '#000000',
                'event_point': '#000080',
                'event_line': '#696969',
                'event_bg': '#F0F8FF',
                'mindmap_center': '#000080',
                'mindmap_branch': '#696969',
                'mindmap_node': '#90EE90',
                'mindmap_sub_branch': '#A9A9A9',
                'mindmap_sub_node': '#F0FFF0',
                'database_comp': '#FFD700',
                'cache_comp': '#FF69B4',
                'queue_comp': '#DA70D6',
                'api_comp': '#87CEEB',
                'service_comp': '#90EE90',
                'connection_arrow': '#000000'
            }
        }
        return themes.get(style, themes['modern'])
    
    async def _save_diagram(self, fig, filename: str, format: str) -> Dict[str, Any]:
        """保存图表"""
        output_path = self.output_dir / f"{filename}_{hash(str(fig))}.{format}"
        
        # 保存文件
        fig.savefig(str(output_path), format=format, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close(fig)
        
        # 转换为base64（可选）
        with open(output_path, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
        
        return {
            'success': True,
            'file_path': str(output_path),
            'base64_data': base64_data,
            'diagram_type': 'custom',
            'title': filename
        }

# 全局图表服务实例
diagram_service = DiagramService()

async def get_diagram_service() -> DiagramService:
    """获取图表服务实例"""
    return diagram_service