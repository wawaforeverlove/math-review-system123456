"""小学六年级数学总复习知识图谱系统 - 主入口"""
import streamlit as st

# ========== 1. 页面配置：必须是第一个Streamlit命令 ==========
st.set_page_config(
    page_title="小学六年级数学总复习系统",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ========== 2. 应用标题和说明 ==========
st.title("🎓 小学六年级数学总复习智能系统")
st.markdown("""
    本系统基于知识图谱技术，为六年级学生提供**个性化、结构化**的总复习解决方案。
    *   **🌳 知识全景**：可视化数学知识体系与关联。
    *   **📝 智能规划**：根据薄弱点生成个性化复习路径。
    *   **🎯 专题突破**：针对重难点进行强化训练。
""")

# ========== 3. 导入和运行主模块 ==========
try:
    from grade_six_main import main as grade_six_main
    grade_six_main()
except ImportError as e:
    st.error(f"❌ 模块导入失败，请确保所有.py文件在正确位置。错误: {e}")
except Exception as e:
    st.error(f"❌ 运行错误: {e}")