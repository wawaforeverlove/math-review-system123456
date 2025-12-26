# grade_six_visualizer.py
class GradeSixVisualizer(KnowledgeVisualizer):
    def __init__(self, graph):
        super().__init__(graph)
        self.review_colors = {
            "数与代数进阶": "#E74C3C",
            "图形与几何深化": "#3498DB", 
            "统计与概率基础": "#9B59B6",
            "综合应用": "#2ECC71"
        }
    
    def create_review_roadmap(self, output_path="review_roadmap.html"):
        """创建六年级复习路线图"""
        net = Network(height="900px", width="100%", directed=True, layout=True)
        
        # 按复习阶段分组
        phases = {
            "第一阶段：数与代数系统复习": ["NA1", "NA2", "NA3", "NA4"],
            "第二阶段：图形几何深化": ["GG1", "GG2", "GG3"],
            "第三阶段：综合能力提升": ["CA1", "CA2", "CA3", "SP1", "SP2"]
        }
        
        y_offset = 0
        for phase_name, nodes in phases.items():
            # 添加阶段标题节点
            net.add_node(
                f"phase_{phase_name}",
                label=phase_name,
                color="#F39C12",
                shape="box",
                size=30,
                x=0,
                y=y_offset,
                physics=False
            )
            
            # 添加该阶段知识点
            x_offset = -200
            for i, node_id in enumerate(nodes):
                node_data = self.graph.nodes[node_id]
                net.add_node(
                    node_id,
                    label=f"{node_id}\n{node_data['name']}",
                    color=self.review_colors.get(node_data['domain'], "#95A5A6"),
                    shape="dot" if not node_data.get('mastered', False) else "star",
                    size=15 + node_data['level'] * 3,
                    x=x_offset + (i % 3) * 200,
                    y=y_offset - 100 - (i // 3) * 150,
                    physics=True,
                    title=self._create_node_tooltip(node_data)
                )
                
                # 连接到阶段标题
                net.add_edge(f"phase_{phase_name}", node_id, dashes=True, width=1)
            
            y_offset -= 400
        
        # 添加阶段间的连接
        net.add_edge("phase_第一阶段：数与代数系统复习", "phase_第二阶段：图形几何深化", 
                    label="为图形计算提供基础", width=2)
        net.add_edge("phase_第二阶段：图形几何深化", "phase_第三阶段：综合能力提升",
                    label="综合运用", width=2)
        
        net.show(output_path)
        return output_path
    
    def create_concept_mindmap(self, central_concept, output_path="concept_mindmap.html"):
        """创建概念思维导图"""
        net = Network(height="800px", width="100%", layout=True)
        
        # 中心概念
        net.add_node(
            central_concept,
            label=f"{central_concept}\n{self.graph.nodes[central_concept]['name']}",
            color="#E74C3C",
            size=50,
            shape="circle"
        )
        
        # 相关概念（前驱）
        prerequisites = list(self.graph.predecessors(central_concept))
        for i, prereq in enumerate(prerequisites):
            angle = 2 * math.pi * i / len(prerequisites)
            x = 300 * math.cos(angle)
            y = 300 * math.sin(angle)
            
            net.add_node(
                prereq,
                label=f"{prereq}\n{self.graph.nodes[prereq]['name']}",
                color="#3498DB",
                size=35,
                x=x,
                y=y,
                physics=True
            )
            net.add_edge(prereq, central_concept, label="先修知识")
        
        # 应用场景（后继）
        applications = list(self.graph.successors(central_concept))
        for i, app in enumerate(applications):
            angle = math.pi + 2 * math.pi * i / len(applications)
            x = 200 * math.cos(angle)
            y = 200 * math.sin(angle)
            
            net.add_node(
                app,
                label=f"{app}\n{self.graph.nodes[app]['name']}",
                color="#2ECC71",
                size=30,
                x=x,
                y=y,
                physics=True
            )
            net.add_edge(central_concept, app, label="应用", color="#27AE60")
        
        # 相似概念
        similar_concepts = []
        for edge in self.graph.edges(central_concept, data=True):
            if edge[2].get('relation') == 'concept_transfer':
                if edge[0] == central_concept:
                    similar_concepts.append(edge[1])
                else:
                    similar_concepts.append(edge[0])
        
        for i, similar in enumerate(similar_concepts):
            angle = math.pi/2 + 2 * math.pi * i / len(similar_concepts)
            x = 400 * math.cos(angle)
            y = 400 * math.sin(angle)
            
            net.add_node(
                similar,
                label=f"{similar}\n{self.graph.nodes[similar]['name']}",
                color="#9B59B6",
                size=30,
                x=x,
                y=y,
                physics=True
            )
            net.add_edge(central_concept, similar, label="知识迁移", dashes=True, color="#8E44AD")
        
        net.show(output_path)
        return output_path