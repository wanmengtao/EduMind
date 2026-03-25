import pandas as pd
from openai import OpenAI
import os

# 从环境变量获取 API Key（如果未设置，则使用备用的）
api_key = os.environ.get("sk-381b621ac9ce4310b94cb182237a218a", "sk-412f5c2771334fd4adc4c81813add67b")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

# 读取特征数据
features = pd.read_csv('student_course_features.csv')
students = pd.read_csv('students.csv')

# 创建报告目录
os.makedirs('reports', exist_ok=True)


def generate_report(student_id, course, row):
    student_name = students[students['student_id'] == student_id]['name'].values[0]

    prompt = f"""
你是一位学情分析专家。请根据以下学生的实验课程学习数据，生成一份学情分析报告。
报告需包含：
1. 学生整体画像（能力、习惯、态度）
2. 优势与薄弱点分析
3. 个性化学习建议
4. 给教师的教学干预建议

数据如下：
- 学生：{student_name}（学号 {student_id}）
- 课程：{course}
- 知识掌握度（测验/作业平均分）：{row['knowledge_mastery']}
- 实验操作能力（综合得分）：{row['lab_ability']}
- 活动频率（每月平均活动次数）：{row['activity_freq']}
- 时间偏好：{row['time_preference']}
- 最终实验报告成绩：{row['final_report_score']}

请用中文输出，语言亲切专业，条理清晰。
"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位学情分析专家。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        report = response.choices[0].message.content
        return report
    except Exception as e:
        return f"生成失败：{str(e)}"


# 为每个学生每门课程生成报告
for _, row in features.iterrows():
    sid = row['student_id']
    course = row['course']
    # 如果缺少关键数据，跳过
    if pd.isna(row['knowledge_mastery']) and pd.isna(row['lab_ability']):
        continue
    report = generate_report(sid, course, row)
    filename = f"reports/{sid}_{course}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"已生成报告：{filename}")

print("所有报告生成完毕！")