import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

st.set_page_config(page_title="智能化学情分析助手", layout="wide")
st.title("📊 智能化学情分析助手")

# 加载数据
@st.cache_data
def load_data():
    students = pd.read_csv('students.csv')
    features = pd.read_csv('student_course_features.csv')
    return students, features

students, features = load_data()

# 侧边栏筛选
st.sidebar.header("筛选条件")
student_list = students['student_id'].tolist()
student_id = st.sidebar.selectbox(
    "选择学生",
    student_list,
    format_func=lambda x: f"{x} - {students[students['student_id']==x]['name'].values[0]}"
)

# 获取该学生的课程列表
student_courses = features[features['student_id'] == student_id]['course'].tolist()
course = st.sidebar.selectbox("选择课程", student_courses)

# 获取对应行数据
row = features[(features['student_id'] == student_id) & (features['course'] == course)].iloc[0]

# 显示关键指标
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("知识掌握度", f"{row['knowledge_mastery']:.1f}" if not pd.isna(row['knowledge_mastery']) else "无数据")
with col2:
    st.metric("实验操作能力", f"{row['lab_ability']:.1f}" if not pd.isna(row['lab_ability']) else "无数据")
with col3:
    st.metric("最终报告成绩", f"{row['final_report_score']:.1f}" if not pd.isna(row['final_report_score']) else "无数据")

st.write(f"**活动频率**：{row['activity_freq']:.1f} 次/月")
st.write(f"**时间偏好**：{'上午' if row['time_preference'] == 'morning' else '下午' if row['time_preference'] == 'afternoon' else '晚上'}")

# 雷达图
st.subheader("📈 能力雷达图")
categories = ['知识掌握度', '实验操作能力', '最终报告成绩']
values = [
    row['knowledge_mastery'] if not pd.isna(row['knowledge_mastery']) else 0,
    row['lab_ability'] if not pd.isna(row['lab_ability']) else 0,
    row['final_report_score'] if not pd.isna(row['final_report_score']) else 0
]
fig = go.Figure(data=go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself'
))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# 显示报告
st.subheader("📝 AI 学情分析报告")
report_path = f"reports/{student_id}_{course}.txt"
if os.path.exists(report_path):
    with open(report_path, 'r', encoding='utf-8') as f:
        report = f.read()
    st.markdown(report)
else:
    st.warning("尚未生成该报告，请先运行 generate_report.py")