import hashlib
import sys
import os
import traceback
import streamlit as st

# 在代码最开头添加一个“验身”标记
st.markdown("""
<div style='background-color: #e6f7ff; padding: 10px; border-radius: 5px; border-left: 5px solid #1890ff;'>
    <b>应用指纹标识:</b> <code>MATH_REVIEW_FULL_VERSION_v2</code> | 如果看到此行，说明完整代码已加载。
</div>
""", unsafe_allow_html=True)


# 显示基本信息
st.write(f"Python 版本: {sys.version}")
st.write(f"工作目录: {os.getcwd()}")


# grade_six_main.py
def main():
    st.set_page_config(page_title="小学六年级数学总复习系统", layout="wide")
    st.title("🎓 小学六年级数学总复习智能系统")
    
    # 初始化六年级专项图谱
    with st.spinner("加载六年级复习知识体系..."):
        kg = GradeSixReviewGraph()
        kg.build_graph()
        kg.build_review_graph()
        visualizer = GradeSixVisualizer(kg.graph)
        recommender = GradeSixReviewRecommender(kg.graph)
    
    # 学生信息收集
    st.sidebar.header("📋 学生信息")
    student_name = st.sidebar.text_input("学生姓名", "张小明")
    
    # 诊断测试结果输入
    st.sidebar.subheader("诊断测试结果")
    weak_areas = st.sidebar.multiselect(
        "薄弱模块",
        options=["分数运算", "百分数应用", "比例问题", "简易方程", 
                "圆的周长面积", "立体图形", "行程问题", "统计图表"],
        default=["分数运算", "简易方程"]
    )
    
    # 映射薄弱模块到知识点ID
    weak_mapping = {
        "分数运算": ["NA1"],
        "百分数应用": ["NA2"],
        "比例问题": ["NA3"],
        "简易方程": ["NA4"],
        "圆的周长面积": ["GG1"],
        "立体图形": ["GG2"],
        "行程问题": ["CA2"],
        "统计图表": ["SP1"]
    }
    
    weak_nodes = []
    for area in weak_areas:
        weak_nodes.extend(weak_mapping.get(area, []))
    
    # 复习目标选择
    st.sidebar.subheader("复习目标")
    review_target = st.sidebar.selectbox(
        "主要目标",
        options=["期末考试冲刺", "薄弱环节突破", "知识体系构建", "小升初备考"],
        index=0
    )
    
    available_days = st.sidebar.slider("可用复习天数", 7, 90, 30)
    
    # 主界面标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "复习全景图", "个性化计划", "专题突破", "模拟测试", "学习报告"
    ])
    
    with tab1:
        st.header("六年级数学知识体系全景")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("生成复习路线图", key="roadmap"):
                roadmap_file = visualizer.create_review_roadmap()
                st.components.v1.html(open(roadmap_file, 'r', encoding='utf-8').read(), height=950)
        
        with col2:
            st.subheader("知识模块分布")
            
            # 统计各模块掌握情况
            domains = {}
            for node in kg.graph.nodes():
                if kg.graph.nodes[node].get('is_review', False):
                    domain = kg.graph.nodes[node]['domain']
                    if domain not in domains:
                        domains[domain] = {"total": 0, "mastered": 0}
                    domains[domain]["total"] += 1
                    if kg.graph.nodes[node].get('mastered', False):
                        domains[domain]["mastered"] += 1
            
            for domain, stats in domains.items():
                progress = stats["mastered"] / stats["total"] if stats["total"] > 0 else 0
                st.write(f"**{domain}**")
                st.progress(progress)
                st.caption(f"{stats['mastered']}/{stats['total']}个知识点")
    
    with tab2:
        st.header("📝 个性化复习计划生成")
        
        # 学生档案
        student_profile = {
            "name": student_name,
            "weaknesses": weak_nodes,
            "target": review_target,
            "available_days": available_days,
            "days_until_exam": available_days
        }
        
        # 策略选择
        strategy = st.radio(
            "选择复习策略",
            options=["weakness_focused", "exam_preparation", "concept_integration"],
            format_func=lambda x: {
                "weakness_focused": "弱项突破",
                "exam_preparation": "考试冲刺",
                "concept_integration": "概念整合"
            }[x],
            horizontal=True
        )
        
        if st.button("生成个性化复习计划", type="primary"):
            with st.spinner("正在为您制定最优复习方案..."):
                plan = recommender.generate_review_plan(student_profile, strategy)
                
                st.success(f"✅ 已为{student_name}生成{available_days}天复习计划")
                
                # 显示计划概览
                st.subheader("📅 复习计划概览")
                
                if strategy == "exam_preparation":
                    for phase, details in plan["schedule"].items():
                        with st.expander(f"**{phase}**"):
                            st.write(f"**重点内容:** {', '.join(details['focus'])}")
                            st.write(f"**练习类型:** {details['practice_type']}")
                            
                            # 显示每日计划
                            st.write("**每日安排:**")
                            for day, daily_plan in details["daily_plan"].items():
                                st.write(f"- {day}: {', '.join(daily_plan['知识点名称'])}")
                
                elif strategy == "weakness_focused":
                    for week, details in plan["schedule"].items():
                        with st.expander(f"**{week}**"):
                            st.write(f"**目标:** {details['目标']}")
                            st.write(f"**知识点:** {', '.join(details['知识点'])}")
                
                # 下载计划
                plan_json = json.dumps(plan, ensure_ascii=False, indent=2)
                st.download_button(
                    label="下载复习计划",
                    data=plan_json,
                    file_name=f"{student_name}_数学复习计划.json",
                    mime="application/json"
                )
    
    with tab3:
        st.header("🎯 专题突破训练")
        
        # 选择专题
        topic = st.selectbox(
            "选择突破专题",
            options=["分数百分数应用题", "行程问题综合", "几何应用", "统计与可能性"],
            index=0
        )
        
        topic_mapping = {
            "分数百分数应用题": "CA1",
            "行程问题综合": "CA2",
            "几何应用": "CA3",
            "统计与可能性": ["SP1", "SP2"]
        }
        
        selected_topic = topic_mapping[topic]
        
        if isinstance(selected_topic, list):
            central_node = selected_topic[0]
        else:
            central_node = selected_topic
        
        # 显示专题知识结构
        st.subheader("专题知识结构")
        
        if st.button("生成思维导图"):
            mindmap_file = visualizer.create_concept_mindmap(central_node)
            st.components.v1.html(open(mindmap_file, 'r', encoding='utf-8').read(), height=850)
        
        # 专题练习
        st.subheader("专题练习建议")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("**基础巩固**")
            st.write("""
            1. 概念辨析题（10道）
            2. 基本计算题（15道）
            3. 公式应用题（8道）
            """)
        
        with col2:
            st.warning("**能力提升**")
            st.write("""
            1. 综合应用题（6道）
            2. 变式训练题（5道）
            3. 易错题专练（8道）
            """)
        
        with col3:
            st.success("**拓展延伸**")
            st.write("""
            1. 生活实际问题（3道）
            2. 跨学科综合题（2道）
            3. 探究性题目（1道）
            """)
    
    with tab4:
        st.header("📝 智能模拟测试")
        
        test_type = st.selectbox(
            "测试类型",
            ["单元测试", "专题测试", "综合模拟", "小升初真题"]
        )
        
        # 生成测试卷
        if st.button("生成模拟试卷"):
            with st.spinner("正在组卷中..."):
                test_paper = generate_test_paper(test_type, weak_nodes)
                
                st.subheader(f"{test_type}试卷")
                
                for i, question in enumerate(test_paper["questions"], 1):
                    with st.expander(f"第{i}题: {question['type']} ({question['score']}分)"):
                        st.write(f"**题目:** {question['content']}")
                        
                        if question['type'] == '选择题':
                            for option in question['options']:
                                st.write(f"- {option}")
                        
                        # 答题区
                        if question['type'] == '选择题':
                            answer = st.radio("请选择:", question['options'], key=f"q{i}")
                        else:
                            answer = st.text_area("请作答:", key=f"q{i}")
                
                if st.button("提交试卷"):
                    st.success("试卷提交成功！系统将自动批改并生成分析报告")
    
    with tab5:
        st.header("📊 学习报告与分析")
        
        # 模拟学习数据
        progress_data = {
            "日期": ["2024-01-01", "2024-01-08", "2024-01-15", "2024-01-22", "2024-01-29"],
            "知识点掌握数": [5, 12, 18, 24, 30],
            "正确率": [0.65, 0.72, 0.78, 0.82, 0.85],
            "学习时长(分钟)": [45, 50, 55, 60, 60]
        }
        
        df = pd.DataFrame(progress_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("学习进步趋势")
            st.line_chart(df.set_index("日期")["正确率"])
        
        with col2:
            st.subheader("知识点掌握情况")
            st.bar_chart(df.set_index("日期")["知识点掌握数"])
        
        # 能力雷达图
        st.subheader("数学能力雷达图")
        
        abilities = {
            "计算能力": 0.82,
            "空间想象": 0.75,
            "逻辑推理": 0.78,
            "问题解决": 0.70,
            "数据分析": 0.80
        }
        
        # 使用plotly创建雷达图
        fig = go.Figure(data=go.Scatterpolar(
            r=list(abilities.values()),
            theta=list(abilities.keys()),
            fill='toself'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 学习建议
        st.subheader("个性化学习建议")
        
        suggestions = {
            "优势保持": ["计算能力较强，保持每日计算练习"],
            "重点突破": [
                "空间想象能力有待提高，建议多进行图形折叠、展开练习",
                "问题解决能力需加强，重点训练应用题审题和策略选择"
            ],
            "学习习惯": [
                "保持当前的学习时长，注意劳逸结合",
                "建议建立错题本，定期回顾易错点"
            ]
        }
        
        for category, items in suggestions.items():
            with st.expander(f"**{category}**"):
                for item in items:
                    st.write(f"• {item}")
