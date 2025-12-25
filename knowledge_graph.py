# knowledge_graph.py
import networkx as nx
from typing import Dict, List, Optional

class MathKnowledgeGraph:
    """基础数学知识图谱类"""
    def __init__(self):
        self.graph = nx.DiGraph()
        self._init_base_curriculum()
        self.build_graph()
    
    def _init_base_curriculum(self):
        """初始化1-6年级基础知识点（简化版）"""
        self.curriculum = {
            "数与代数": [
                {"id": "N1", "name": "20以内数的认识", "level": 1, "prerequisites": []},
                {"id": "N2", "name": "100以内数的认识", "level": 1, "prerequisites": ["N1"]},
                {"id": "N3", "name": "加减法运算", "level": 1, "prerequisites": ["N1", "N2"]},
                {"id": "N4", "name": "乘除法初步", "level": 2, "prerequisites": ["N3"]},
                {"id": "N5", "name": "分数初步认识", "level": 3, "prerequisites": ["N4"]},
                {"id": "N6", "name": "小数初步认识", "level": 3, "prerequisites": ["N4"]},
            ],
            "图形与几何": [
                {"id": "G1", "name": "立体图形直观认识", "level": 1, "prerequisites": []},
                {"id": "G2", "name": "平面图形认识", "level": 1, "prerequisites": ["G1"]},
                {"id": "G3", "name": "周长与面积", "level": 3, "prerequisites": ["G2"]},
            ]
        }
    
    def build_graph(self):
        """构建基础图谱结构"""
        for domain, topics in self.curriculum.items():
            for topic in topics:
                self.graph.add_node(
                    topic["id"],
                    name=topic["name"],
                    domain=domain,
                    level=topic["level"],
                    mastered=False
                )
                for prereq in topic["prerequisites"]:
                    self.graph.add_edge(prereq, topic["id"], relation="prerequisite")
        return self.graph


class GradeSixReviewGraph(MathKnowledgeGraph):
    """六年级总复习专项知识图谱（扩展类）"""
    def __init__(self):
        super().__init__()  # 继承基础图谱
        self.extended_curriculum = {
            "数与代数进阶": [
                {
                    "id": "NA1",
                    "name": "分数四则混合运算",
                    "level": 4,
                    "prerequisites": ["N5", "N6"],
                    "keywords": ["通分", "约分", "运算顺序"],
                    "common_errors": ["运算顺序错误", "通分不彻底"]
                },
                {
                    "id": "NA2",
                    "name": "百分数的应用",
                    "level": 4,
                    "prerequisites": ["NA1"],
                    "keywords": ["利率", "折扣", "增长率"],
                    "cross_refs": ["SP1"]
                },
                {
                    "id": "NA3",
                    "name": "比例与正反比例",
                    "level": 5,
                    "prerequisites": ["NA2"],
                    "keywords": ["比例关系", "比例尺", "正比例", "反比例"]
                },
            ],
            "图形与几何深化": [
                {
                    "id": "GG1",
                    "name": "圆与扇形",
                    "level": 5,
                    "prerequisites": ["G3"],
                    "keywords": ["圆周率", "圆的周长", "圆的面积"],
                    "formulas": ["C=πd=2πr", "S=πr²"]
                },
                {
                    "id": "GG2",
                    "name": "立体图形的表面积与体积",
                    "level": 6,
                    "prerequisites": ["G3", "GG1"],
                    "keywords": ["长方体", "圆柱", "圆锥", "表面积", "体积"]
                },
            ],
            "统计与概率基础": [
                {
                    "id": "SP1",
                    "name": "统计图表综合应用",
                    "level": 4,
                    "prerequisites": ["NA2"],
                    "keywords": ["扇形统计图", "折线统计图", "数据分析"]
                },
            ]
        }
        self.build_review_graph()
    
    def build_review_graph(self):
        """构建六年级总复习专项图谱"""
        # 添加扩展节点
        for domain, topics in self.extended_curriculum.items():
            for topic in topics:
                self.graph.add_node(
                    topic["id"],
                    name=topic["name"],
                    domain=domain,
                    level=topic["level"],
                    mastered=False,
                    is_review=True,
                    keywords=topic.get("keywords", []),
                    common_errors=topic.get("common_errors", [])
                )
                # 添加先修关系
                for prereq in topic["prerequisites"]:
                    self.graph.add_edge(prereq, topic["id"], relation="prerequisite", weight=1.0)
        
        # 建立关键跨领域关联
        self.graph.add_edge("NA2", "SP1", relation="supports", weight=0.8)
        print("六年级复习知识图谱构建完成，总节点数：", len(self.graph.nodes))
        return self.graph
    
    def find_prerequisites(self, node_id: str) -> List[str]:
        """查找某个知识点的所有先修知识点"""
        if node_id not in self.graph:
            return []
        return list(nx.ancestors(self.graph, node_id))
    
    def get_review_topics(self, domain: Optional[str] = None) -> List[Dict]:
        """获取复习知识点列表，可按领域筛选"""
        topics = []
        for node_id, data in self.graph.nodes(data=True):
            if data.get('is_review'):
                if domain is None or data['domain'] == domain:
                    topics.append({"id": node_id, **data})
        return topics


# 以下代码用于快速测试这个文件是否能正常运行
if __name__ == "__main__":
    print("正在测试知识图谱模块...")
    kg = GradeSixReviewGraph()
    print(f"图谱包含 {len(kg.graph.nodes)} 个知识点")
    print(f"其中标记为复习的知识点有 {len(kg.get_review_topics())} 个")
    print("\n‘分数四则混合运算(NA1)’的先修知识点有：")
    for prereq in kg.find_prerequisites("NA1"):
        print(f"  - {prereq}: {kg.graph.nodes[prereq]['name']}")
    print("\n测试完成！")