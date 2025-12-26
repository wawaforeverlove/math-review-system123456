# extended_knowledge_graph.py
class GradeSixReviewGraph(MathKnowledgeGraph):
    def __init__(self):
        super().__init__()
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
                    "prerequisites": ["NA1", "N6"],
                    "keywords": ["利率", "折扣", "增长率", "百分比"],
                    "cross_refs": ["SP1"]  # 关联统计图表
                },
                {
                    "id": "NA3", 
                    "name": "比例与正反比例", 
                    "level": 5,
                    "prerequisites": ["NA1", "NA2"],
                    "keywords": ["比例关系", "比例尺", "正比例", "反比例"],
                    "real_world": ["地图比例尺", "溶液浓度"]
                },
                {
                    "id": "NA4", 
                    "name": "简易方程", 
                    "level": 5,
                    "prerequisites": ["N3", "NA1"],
                    "keywords": ["方程", "未知数", "等式性质"],
                    "problem_types": ["和差倍问题", "行程问题", "工程问题"]
                }
            ],
            "图形与几何深化": [
                {
                    "id": "GG1",
                    "name": "圆与扇形",
                    "level": 5,
                    "prerequisites": ["G3"],
                    "keywords": ["圆周率", "圆的周长", "圆的面积", "扇形"],
                    "formulas": ["C=πd=2πr", "S=πr²"]
                },
                {
                    "id": "GG2",
                    "name": "立体图形的表面积与体积",
                    "level": 6,
                    "prerequisites": ["G3", "GG1"],
                    "keywords": ["长方体", "正方体", "圆柱", "圆锥", "表面积", "体积"],
                    "formulas": ["V长方体=abc", "V圆柱=πr²h", "V圆锥=1/3πr²h"]
                },
                {
                    "id": "GG3",
                    "name": "图形的运动与变换",
                    "level": 4,
                    "prerequisites": ["G1"],
                    "keywords": ["平移", "旋转", "轴对称", "图形的放大与缩小"],
                    "visualization": ["对称轴", "旋转中心", "平移方向"]
                }
            ],
            "统计与概率基础": [
                {
                    "id": "SP1",
                    "name": "统计图表综合应用",
                    "level": 4,
                    "prerequisites": ["NA2"],
                    "keywords": ["扇形统计图", "折线统计图", "条形统计图", "数据分析"],
                    "interpretation": ["读取数据", "趋势分析", "得出结论"]
                },
                {
                    "id": "SP2",
                    "name": "可能性初步",
                    "level": 4,
                    "prerequisites": ["NA1"],
                    "keywords": ["可能性", "概率", "等可能性", "游戏公平性"],
                    "applications": ["抽奖", "游戏设计", "预测"]
                }
            ],
            "综合应用": [
                {
                    "id": "CA1",
                    "name": "分数百分数应用题",
                    "level": 6,
                    "prerequisites": ["NA1", "NA2", "NA4"],
                    "problem_types": ["浓度问题", "利润问题", "工程问题"],
                    "strategies": ["单位1法", "量率对应", "方程法"]
                },
                {
                    "id": "CA2",
                    "name": "行程问题综合",
                    "level": 6,
                    "prerequisites": ["NA3", "NA4"],
                    "problem_types": ["相遇问题", "追及问题", "流水行船"],
                    "strategies": ["线段图法", "方程法", "比例法"]
                },
                {
                    "id": "CA3",
                    "name": "几何应用题",
                    "level": 6,
                    "prerequisites": ["GG1", "GG2"],
                    "problem_types": ["包装问题", "容器问题", "材料计算"],
                    "strategies": ["空间想象", "公式应用", "最优方案"]
                }
            ]
        }
    
    def build_review_graph(self):
        """构建六年级总复习专项图谱"""
        # 添加新节点
        for domain, topics in self.extended_curriculum.items():
            for topic in topics:
                self.graph.add_node(
                    topic["id"],
                    name=topic["name"],
                    domain=domain,
                    level=topic["level"],
                    mastered=False,
                    is_review=True,  # 标记为复习知识点
                    keywords=topic.get("keywords", []),
                    problem_types=topic.get("problem_types", []),
                    common_errors=topic.get("common_errors", [])
                )
                
                # 添加先修关系
                for prereq in topic["prerequisites"]:
                    self.graph.add_edge(prereq, topic["id"], relation="prerequisite", weight=1.0)
        
        # 建立跨模块强关联
        self._build_cross_module_links()
        
        # 建立知识迁移关系（相似知识点关联）
        self._build_knowledge_transfer_links()
    
    def _build_cross_module_links(self):
        """建立跨模块知识关联"""
        # 百分数与统计图表的关联
        self.graph.add_edge("NA2", "SP1", relation="supports", weight=0.8)
        
        # 比例与图形缩放的关联
        self.graph.add_edge("NA3", "GG3", relation="applies_to", weight=0.7)
        
        # 方程与各类应用题的关联
        self.graph.add_edge("NA4", "CA1", relation="solves", weight=0.9)
        self.graph.add_edge("NA4", "CA2", relation="solves", weight=0.9)
    
    def _build_knowledge_transfer_links(self):
        """建立知识迁移关系（相似概念关联）"""
        # 分数、小数、百分数的概念迁移
        self.graph.add_edge("N5", "N6", relation="concept_transfer", weight=0.6)
        self.graph.add_edge("N5", "NA2", relation="concept_transfer", weight=0.7)
        
        # 平面图形面积与立体图形表面积的迁移
        self.graph.add_edge("G3", "GG2", relation="concept_transfer", weight=0.8)