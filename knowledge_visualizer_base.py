"""知识图谱可视化基类"""
import streamlit as st
import math

class KnowledgeVisualizer:
    """知识图谱可视化基类"""
    def __init__(self, graph):
        self.graph = graph
    
    def _create_node_tooltip(self, node_data):
        """创建节点提示信息"""
        tooltip = f"名称: {node_data['name']}<br>"
        tooltip += f"领域: {node_data.get('domain', '未知')}<br>"
        tooltip += f"难度等级: {node_data.get('level', '未知')}<br>"
        
        if 'keywords' in node_data:
            tooltip += f"关键词: {', '.join(node_data['keywords'])}<br>"
        
        if 'common_errors' in node_data:
            tooltip += f"常见错误: {', '.join(node_data['common_errors'])}<br>"
        
        return tooltip