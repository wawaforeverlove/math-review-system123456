"""学习路径推荐基类"""
import streamlit as st
import networkx as nx
from typing import Dict, List, Optional

class LearningPathRecommender:
    """学习路径推荐基类"""
    def __init__(self, graph):
        self.graph = graph
    
    def get_prerequisite_tree(self, node_id: str) -> Dict:
        """获取先修知识树"""
        if node_id not in self.graph:
            return {}
        
        tree = {}
        for pred in self.graph.predecessors(node_id):
            tree[pred] = self.get_prerequisite_tree(pred)
        
        return tree
    
    def _flatten_prereq_tree(self, tree: Dict) -> List[str]:
        """展平先修知识树"""
        nodes = []
        for node, subtree in tree.items():
            nodes.append(node)
            nodes.extend(self._flatten_prereq_tree(subtree))
        return list(set(nodes))