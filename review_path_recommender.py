# review_path_recommender.py
class GradeSixReviewRecommender(LearningPathRecommender):
    def __init__(self, graph):
        super().__init__(graph)
        self.review_strategies = {
            "weakness_focused": self._weakness_focused_path,
            "exam_preparation": self._exam_preparation_path,
            "concept_integration": self._concept_integration_path
        }
    
    def generate_review_plan(self, student_profile: Dict, strategy: str = "exam_preparation") -> Dict:
        """
        生成个性化复习计划
        
        Args:
            student_profile: 包含学生弱点和目标的信息
            strategy: 复习策略类型
        """
        if strategy not in self.review_strategies:
            raise ValueError(f"不支持的复习策略: {strategy}")
        
        return self.review_strategies[strategy](student_profile)
    
    def _weakness_focused_path(self, profile: Dict) -> Dict:
        """弱项突破型复习路径"""
        weaknesses = profile.get("weaknesses", [])
        target_days = profile.get("target_days", 30)
        
        # 对每个弱项知识点，找到其先修基础
        foundation_nodes = set()
        for weak in weaknesses:
            prereqs = nx.ancestors(self.graph, weak)
            foundation_nodes.update(prereqs)
        
        # 按领域和难度组织复习内容
        review_schedule = self._organize_by_week(foundation_nodes, weaknesses, target_days)
        
        return {
            "strategy": "弱项突破",
            "total_days": target_days,
            "weaknesses": weaknesses,
            "schedule": review_schedule,
            "assessment_points": self._set_assessment_points(review_schedule)
        }
    
    def _exam_preparation_path(self, profile: Dict) -> Dict:
        """考试冲刺型复习路径"""
        exam_topics = [
            "NA1", "NA2", "NA4",  # 数与代数核心
            "GG1", "GG2",         # 图形几何核心
            "CA1", "CA2", "CA3",  # 综合应用
            "SP1"                 # 统计
        ]
        
        # 构建倒计时复习计划（考前30天）
        days_until_exam = profile.get("days_until_exam", 30)
        
        schedule = {
            "第一阶段：知识梳理（第1-10天）": {
                "focus": ["NA1", "NA2", "GG1", "GG2"],
                "daily_plan": self._create_daily_plan(["NA1", "NA2", "GG1", "GG2"], 10),
                "practice_type": "基础题+概念辨析"
            },
            "第二阶段：综合提升（第11-20天）": {
                "focus": ["NA4", "CA1", "CA2", "CA3"],
                "daily_plan": self._create_daily_plan(["NA4", "CA1", "CA2", "CA3"], 10),
                "practice_type": "应用题+综合题"
            },
            "第三阶段：模拟冲刺（第21-30天）": {
                "focus": exam_topics,
                "daily_plan": self._create_daily_plan(exam_topics, 10),
                "practice_type": "模拟卷+错题回顾"
            }
        }
        
        return {
            "strategy": "考试冲刺",
            "total_phases": 3,
            "days_per_phase": 10,
            "schedule": schedule,
            "mock_exam_schedule": [10, 20, 25, 28, 30]  # 模拟考试日期
        }
    
    def _concept_integration_path(self, profile: Dict) -> Dict:
        """概念整合型复习路径"""
        # 识别跨领域知识簇
        concept_clusters = {
            "数的扩展": ["N5", "N6", "NA1", "NA2"],  # 分数→小数→百分数
            "图形度量": ["G3", "GG1", "GG2"],        # 面积→圆→立体图形
            "问题解决": ["NA4", "CA1", "CA2", "CA3"]  # 方程→各类应用题
        }
        
        integration_path = []
        for cluster_name, nodes in concept_clusters.items():
            # 在每个簇内建立学习路径
            cluster_path = []
            for node in nodes:
                prereq_tree = self.get_prerequisite_tree(node)
                cluster_path.append({
                    "concept": node,
                    "name": self.graph.nodes[node]["name"],
                    "prerequisite_count": len(self._flatten_prereq_tree(prereq_tree))
                })
            
            # 按先修关系排序
            cluster_path.sort(key=lambda x: x["prerequisite_count"])
            
            integration_path.append({
                "cluster": cluster_name,
                "description": self._get_cluster_description(cluster_name),
                "learning_path": cluster_path,
                "integration_activities": self._get_integration_activities(cluster_name)
            })
        
        return {
            "strategy": "概念整合",
            "concept_clusters": integration_path,
            "integration_projects": self._design_integration_projects()
        }
    
    def _organize_by_week(self, foundation_nodes, weak_nodes, total_days):
        """按周组织复习计划"""
        weeks = total_days // 7
        schedule = {}
        
        # 第一周：基础巩固
        schedule["第1周：基础巩固"] = {
            "目标": "夯实弱项知识点的基础",
            "知识点": list(foundation_nodes)[:5],  # 取最重要的5个基础点
            "每日安排": self._distribute_to_days(list(foundation_nodes)[:5], 7),
            "配套练习": "基础题+概念判断题"
        }
        
        # 中间周：弱项突破
        for week in range(2, weeks):
            schedule[f"第{week}周：专项突破"] = {
                "目标": f"集中攻克第{week-1}个弱项",
                "知识点": weak_nodes[week-2:week] if week-2 < len(weak_nodes) else [],
                "每日安排": self._distribute_to_days(weak_nodes[week-2:week], 7),
                "配套练习": "专项训练题+易错题"
            }
        
        # 最后一周：综合应用
        schedule[f"第{weeks}周：综合应用"] = {
            "目标": "综合运用所学知识解决问题",
            "知识点": weak_nodes + list(foundation_nodes)[-3:],
            "每日安排": self._distribute_to_days(weak_nodes, 7),
            "配套练习": "综合应用题+模拟题"
        }
        
        return schedule
    
    def _create_daily_plan(self, topics, days):
        """创建每日学习计划"""
        daily_plans = {}
        topics_per_day = max(1, len(topics) // days)
        
        for day in range(1, days + 1):
            start_idx = (day - 1) * topics_per_day
            end_idx = min(start_idx + topics_per_day, len(topics))
            daily_topics = topics[start_idx:end_idx]
            
            daily_plans[f"第{day}天"] = {
                "复习内容": daily_topics,
                "知识点名称": [self.graph.nodes[t]["name"] for t in daily_topics],
                "学习时长": "60-90分钟",
                "练习建议": {
                    "基础巩固": f"{len(daily_topics)*5}道基础题",
                    "能力提升": f"{len(daily_topics)*2}道应用题",
                    "易错回顾": "回顾前日错题"
                }
            }
        
        return daily_plans