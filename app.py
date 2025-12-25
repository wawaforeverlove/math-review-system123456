import hashlib
import sys
import os
import traceback
import streamlit as st
import json, pandas as pd, plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np
import json
from typing import Dict, List, Optional
import random

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

"""
小学六年级数学总复习知识图谱系统
功能：
1. 展示知识图谱（树状结构）
2. 知识点详细讲解
3. 练习题生成
4. 错题本功能
"""



# 设置页面配置（必须放在最前面）
st.set_page_config(
    page_title="小学六年级数学总复习系统",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== 知识点数据 ==================
KNOWLEDGE_GRAPH = {
    "六年级数学总复习": {
        "数与代数": {
            "分数": {
                "分数的意义与性质": ["分数的意义", "分数单位", "分数的基本性质"],
                "分数的运算": ["同分母分数加减", "异分母分数加减", "分数乘除法"],
                "分数应用题": ["求一个数的几分之几", "已知一个数的几分之几求这个数"]
            },
            "小数": {
                "小数的意义与性质": ["小数的意义", "小数的基本性质", "小数点的移动"],
                "小数的运算": ["小数加减法", "小数乘除法"],
                "小数应用题": ["购物问题", "测量问题"]
            },
            "百分数": {
                "百分数的意义": ["百分数的读写", "百分数与小数分数的互化"],
                "百分数应用题": ["求百分率", "求一个数的百分之几", "折扣与税率"]
            },
            "比和比例": {
                "比的意义和性质": ["比的意义", "比的基本性质", "化简比"],
                "比例的意义和性质": ["比例的意义", "比例的基本性质"],
                "正比例和反比例": ["正比例关系", "反比例关系"]
            }
        },
        "图形与几何": {
            "平面图形": {
                "周长与面积": ["长方形和正方形的周长面积", "三角形、平行四边形、梯形的面积", "圆的周长和面积"],
                "图形的变换": ["平移、旋转、对称", "图形的放大与缩小"]
            },
            "立体图形": {
                "表面积与体积": ["长方体和正方体的表面积体积", "圆柱的表面积体积", "圆锥的体积"],
                "视图与展开图": ["三视图", "立体图形的展开图"]
            },
            "图形的位置与运动": ["位置与方向", "图形的平移与旋转", "轴对称图形"]
        },
        "统计与概率": {
            "统计": ["统计表", "条形统计图", "折线统计图", "扇形统计图"],
            "概率": ["可能性", "简单的概率计算"]
        },
        "解决问题": {
            "数量关系": ["归一问题", "归总问题", "和差倍问题", "行程问题"],
            "策略与方法": ["列表法", "画图法", "假设法", "方程法"]
        }
>>>>>>> Stashed changes
    }
}

# ================== 知识点详细内容 ==================
KNOWLEDGE_CONTENT = {
    "分数的意义": {
        "讲解": """
        ## 分数的意义
        
        分数表示一个整体被平均分成若干份，表示这样的一份或几份的数。
        
        ### 关键概念：
        1. **整体**：被分的对象
        2. **平均分**：每份大小相等
        3. **分母**：表示平均分的份数
        4. **分子**：表示取的份数
        
        ### 例子：
        - 把一个月饼平均分成4份，每份是1/4
        - 一个班级有40人，男生有23人，男生占全班的23/40
        """,
        "例题": """
        **例题**：小明有12颗糖，他吃了1/3，吃了多少颗？
        
        **解答**：
        12 × 1/3 = 4（颗）
        答：吃了4颗糖。
        """,
        "练习题": ["3/5表示的意义是什么？", "把20个苹果平均分成5份，每份是几分之几？", "1/4 + 2/4 = ?"]
    },
    "圆的周长和面积": {
        "讲解": """
        ## 圆的周长和面积
        
        ### 圆的周长
        公式：C = πd 或 C = 2πr
        
        ### 圆的面积
        公式：S = πr²
        
        ### 重要概念：
        - π（圆周率）≈ 3.14
        - d（直径）= 2r
        - r（半径）= d ÷ 2
        
        ### 记忆口诀：
        "圆的周长π乘d，或2πr要记清；
         圆的面积πr²，半径平方要分明。"
        """,
        "例题": """
        **例题**：一个圆的半径是5cm，求它的周长和面积。
        
        **解答**：
        周长：C = 2 × 3.14 × 5 = 31.4（cm）
        面积：S = 3.14 × 5² = 3.14 × 25 = 78.5（cm²）
        """,
        "练习题": ["直径10cm的圆周长是多少？", "半径3m的圆面积是多少？", "周长62.8cm的圆半径是多少？"]
    },
    "百分数的意义": {
        "讲解": """
        ## 百分数的意义
        
        百分数表示一个数是另一个数的百分之几，也叫百分率或百分比。
        
        ### 表示方法：
        - 用"%"表示
        - 如：25% 表示百分之二十五
        
        ### 百分数与分数、小数的互化：
        1. 百分数化小数：去掉%，除以100
        2. 小数化百分数：乘以100，加上%
        3. 百分数化分数：写成分母是100的分数，再化简
        
        ### 实际应用：
        - 折扣：八折 = 80%
        - 合格率：合格产品占全部产品的百分之几
        - 增长率：增长的部分占原来的百分之几
        """,
        "例题": """
        **例题**：某商品原价200元，打八五折出售，现价多少元？
        
        **解答**：
        200 × 85% = 200 × 0.85 = 170（元）
        答：现价170元。
        """,
        "练习题": ["把0.75化成百分数", "把60%化成小数", "一件衣服打七折后210元，原价多少？"]
    }
}

# ================== 练习题数据库 ==================
PRACTICE_QUESTIONS = {
    "分数": [
        {"题目": "3/4 + 1/4 = ?", "选项": ["1", "4/4", "1/2", "2/4"], "答案": "1", "难度": "简单"},
        {"题目": "2/3 × 3/5 = ?", "选项": ["2/5", "6/15", "1", "5/8"], "答案": "2/5", "难度": "中等"},
        {"题目": "小明有3/5米绳子，用了1/4米，还剩多少米？", "选项": ["7/20", "1/2", "2/5", "3/10"], "答案": "7/20", "难度": "中等"}
    ],
    "小数": [
        {"题目": "2.5 + 3.7 = ?", "选项": ["6.2", "5.2", "6.0", "5.8"], "答案": "6.2", "难度": "简单"},
        {"题目": "4.8 × 0.5 = ?", "选项": ["2.4", "9.6", "0.24", "24"], "答案": "2.4", "难度": "简单"}
    ],
    "百分数": [
        {"题目": "把0.65化成百分数", "选项": ["65%", "6.5%", "650%", "0.65%"], "答案": "65%", "难度": "简单"},
        {"题目": "一件商品原价80元，打九折后多少钱？", "选项": ["72元", "64元", "88元", "90元"], "答案": "72元", "难度": "简单"}
    ],
    "图形": [
        {"题目": "长方形的长8cm，宽5cm，面积是多少？", "选项": ["40cm²", "13cm²", "26cm²", "20cm²"], "答案": "40cm²", "难度": "简单"},
        {"题目": "圆的半径3cm，周长约是多少？（π≈3.14）", "选项": ["18.84cm", "9.42cm", "28.26cm", "6.28cm"], "答案": "18.84cm", "难度": "中等"}
    ]
}

# ================== 辅助函数 ==================
def display_knowledge_tree(data: Dict, level: int = 0):
    """递归显示知识树"""
    for key, value in data.items():
        if isinstance(value, dict):
            with st.expander(f"{'📁' if level == 0 else '📘'} {key}"):
                display_knowledge_tree(value, level + 1)
        elif isinstance(value, list):
            for item in value:
                if st.button(f"🔹 {item}", key=f"btn_{item}"):
                    st.session_state.selected_topic = item
        else:
            st.write(f"📝 {value}")

def generate_practice_questions(topic: str, num: int = 3):
    """生成练习题"""
    questions = []
    all_topics = list(PRACTICE_QUESTIONS.keys())
    
    if topic in PRACTICE_QUESTIONS:
        pool = PRACTICE_QUESTIONS[topic]
    else:
        # 如果指定主题没有题目，从所有题目中随机选择
        pool = []
        for t in all_topics:
            pool.extend(PRACTICE_QUESTIONS[t])
    
    if len(pool) > num:
        questions = random.sample(pool, num)
    else:
        questions = pool
    
    return questions

# ================== 初始化Session State ==================
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = None
if 'wrong_questions' not in st.session_state:
    st.session_state.wrong_questions = []
if 'practice_mode' not in st.session_state:
    st.session_state.practice_mode = False

# ================== 侧边栏 ==================
with st.sidebar:
    st.title("🧮 导航菜单")
    
    menu = st.radio(
        "选择功能",
        ["知识图谱", "知识点讲解", "智能练习", "错题本", "学习进度"]
    )
    
    st.markdown("---")
    st.subheader("📊 学习统计")
    st.metric("已掌握知识点", "12", "+3")
    st.metric("练习正确率", "85%", "5%")
    st.metric("学习时长", "8小时", "2小时")
    
    st.markdown("---")
    st.caption("小学六年级数学总复习系统 v1.0")

# ================== 主页面 ==================
st.title("🧮 小学六年级数学总复习系统")
st.markdown("### 构建知识体系，掌握数学核心概念")

# 根据菜单选择显示不同内容
if menu == "知识图谱":
    st.header("🌳 知识图谱")
    st.info("点击展开查看详细知识点结构")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        display_knowledge_tree(KNOWLEDGE_GRAPH)
    
    with col2:
        st.subheader("📌 快速导航")
        topics = ["分数运算", "百分数应用", "圆的面积", "长方体体积", "统计图"]
        for topic in topics:
            if st.button(topic, type="secondary"):
                st.session_state.selected_topic = topic

elif menu == "知识点讲解":
    st.header("📚 知识点详细讲解")
    
    if st.session_state.selected_topic:
        topic = st.session_state.selected_topic
        st.success(f"当前学习：{topic}")
        
        if topic in KNOWLEDGE_CONTENT:
            content = KNOWLEDGE_CONTENT[topic]
            
            tabs = st.tabs(["详细讲解", "例题解析", "巩固练习"])
            
            with tabs[0]:
                st.markdown(content["讲解"])
            
            with tabs[1]:
                st.markdown(content["例题"])
            
            with tabs[2]:
                st.write("**练习题：**")
                for i, question in enumerate(content["练习题"], 1):
                    st.write(f"{i}. {question}")
                
                user_answer = st.text_area("写下你的解答：")
                if st.button("提交答案"):
                    if user_answer:
                        st.success("已提交！正确答案稍后公布")
                    else:
                        st.warning("请先写下你的解答")
        else:
            st.warning(f"知识点 '{topic}' 的详细内容正在建设中...")
            st.info("你可以尝试选择其他知识点")
    else:
        st.info("请从知识图谱中选择一个知识点开始学习")
        
        # 显示热门知识点
        st.subheader("🔥 热门知识点")
        cols = st.columns(3)
        hot_topics = ["分数的意义", "圆的周长和面积", "百分数的意义"]
        
        for i, topic in enumerate(hot_topics):
            with cols[i]:
                if st.button(f"学习 {topic}"):
                    st.session_state.selected_topic = topic
                    st.rerun()

elif menu == "智能练习":
    st.header("💪 智能练习")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("练习设置")
        topic = st.selectbox(
            "选择练习主题",
            ["分数", "小数", "百分数", "图形", "混合练习"]
        )
        difficulty = st.select_slider(
            "难度",
            options=["简单", "中等", "困难"]
        )
        question_num = st.slider("题目数量", 1, 10, 5)
        
        if st.button("生成练习", type="primary"):
            st.session_state.practice_mode = True
            st.session_state.current_questions = generate_practice_questions(topic, question_num)
            st.session_state.current_answers = [None] * len(st.session_state.current_questions)
            st.session_state.show_answers = False
    
    with col2:
        if st.session_state.practice_mode and 'current_questions' in st.session_state:
            st.subheader("📝 练习题")
            
            questions = st.session_state.current_questions
            
            for i, q in enumerate(questions):
                st.markdown(f"**第{i+1}题：** {q['题目']}")
                
                # 选择题显示选项
                if '选项' in q:
                    selected = st.radio(
                        f"选择答案：",
                        q['选项'],
                        key=f"q_{i}"
                    )
                    st.session_state.current_answers[i] = selected
                else:
                    # 填空题
                    answer = st.text_input(f"请输入答案：", key=f"q_{i}")
                    st.session_state.current_answers[i] = answer
                
                st.markdown("---")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("提交答案", type="primary"):
                    correct_count = 0
                    for i, q in enumerate(questions):
                        if st.session_state.current_answers[i] == q['答案']:
                            correct_count += 1
                        else:
                            # 添加到错题本
                            st.session_state.wrong_questions.append({
                                "题目": q['题目'],
                                "你的答案": st.session_state.current_answers[i],
                                "正确答案": q['答案']
                            })
                    
                    st.success(f"答对了 {correct_count}/{len(questions)} 题")
                    st.session_state.show_answers = True
            
            with col_btn2:
                if st.button("重新练习"):
                    st.session_state.practice_mode = False
                    st.rerun()
            
            # 显示答案
            if st.session_state.get('show_answers', False):
                st.subheader("📋 正确答案")
                for i, q in enumerate(questions):
                    st.write(f"第{i+1}题：{q['题目']}")
                    st.write(f"正确答案：**{q['答案']}**")
                    st.write(f"你的答案：{st.session_state.current_answers[i]}")
                    if st.session_state.current_answers[i] == q['答案']:
                        st.success("✓ 正确")
                    else:
                        st.error("✗ 错误")
                    st.markdown("---")
        else:
            st.info("请先设置练习参数并点击'生成练习'按钮")

elif menu == "错题本":
    st.header("📖 错题本")
    
    if st.session_state.wrong_questions:
        st.warning(f"你有 {len(st.session_state.wrong_questions)} 道错题需要复习")
        
        for i, item in enumerate(st.session_state.wrong_questions):
            with st.expander(f"错题 {i+1}"):
                st.write(f"**题目：** {item['题目']}")
                st.write(f"**你的答案：** {item['你的答案']}")
                st.write(f"**正确答案：** {item['正确答案']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("标记为已掌握", key=f"master_{i}"):
                        st.session_state.wrong_questions.pop(i)
                        st.success("已从错题本移除")
                        st.rerun()
                with col2:
                    if st.button("再做一遍", key=f"redo_{i}"):
                        st.info("重新练习这道题...")
        
        if st.button("清空错题本", type="secondary"):
            st.session_state.wrong_questions = []
            st.success("错题本已清空")
            st.rerun()
    else:
        st.success("🎉 太棒了！错题本为空")
        st.info("继续保持，认真学习每一道题")

elif menu == "学习进度":
    st.header("📈 学习进度")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("知识点掌握情况")
        # 模拟进度数据
        progress_data = {
            "数与代数": 75,
            "图形与几何": 60,
            "统计与概率": 85,
            "解决问题": 50
        }
        
        for topic, percent in progress_data.items():
            st.write(f"**{topic}**")
            st.progress(percent / 100)
            st.write(f"{percent}% 掌握")
            st.markdown("---")
    
    with col2:
        st.subheader("学习统计")
        
        # 模拟周学习数据
        import plotly.graph_objects as go
        
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        study_time = [30, 45, 60, 25, 50, 90, 40]  # 分钟
        
        fig = go.Figure(data=[
            go.Bar(x=days, y=study_time, marker_color='lightblue')
        ])
        
        fig.update_layout(
            title="本周学习时长（分钟）",
            xaxis_title="日期",
            yaxis_title="学习时长（分钟）",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 🏆 学习成就")
        achievements = [
            "连续学习3天 ✓",
            "完成20道练习题 ✓",
            "掌握分数运算 ✓",
            "图形与几何学习中...",
            "挑战难题 ×"
        ]
        
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
    if __name__ == "__main__": main()
