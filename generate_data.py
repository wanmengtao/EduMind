import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime

fake = Faker('zh_CN')

# 配置参数
num_students = 30
courses = ['电路分析实验', '信号处理实验', '嵌入式系统实验']
start_date = datetime(2025, 9, 1)
end_date = datetime(2025, 12, 31)

np.random.seed(42)
random.seed(42)

# 学生基本信息
students = []
for i in range(num_students):
    students.append({
        'student_id': f'S{20250001 + i}',
        'name': fake.name(),
        'gender': random.choice(['男', '女']),
        'major': random.choice(['电子信息工程', '通信工程', '自动化'])
    })
students_df = pd.DataFrame(students)

# 学习行为记录（过程性）
behavior_records = []
for course in courses:
    for student in students:
        num_records = random.randint(8, 15)
        for _ in range(num_records):
            record_date = fake.date_between(start_date=start_date, end_date=end_date)
            activity_type = random.choice(['实验操作', '作业提交', '课堂互动', '测验'])
            if activity_type == '实验操作':
                score = np.clip(np.random.normal(75, 15), 0, 100)
                error_count = np.random.poisson(2) if score < 60 else np.random.poisson(0.5)
                time_spent = np.random.normal(45, 10)
            elif activity_type == '作业提交':
                score = np.clip(np.random.normal(80, 12), 0, 100)
                error_count = None
                time_spent = None
            elif activity_type == '课堂互动':
                score = random.randint(0, 5) * 20
                error_count = None
                time_spent = None
            else:  # 测验
                score = np.clip(np.random.normal(70, 18), 0, 100)
                error_count = None
                time_spent = None

            behavior_records.append({
                'student_id': student['student_id'],
                'course': course,
                'date': record_date,
                'activity_type': activity_type,
                'score': score,
                'error_count': error_count,
                'time_spent_min': time_spent
            })

behavior_df = pd.DataFrame(behavior_records)

# 最终实验报告成绩（终结性）
final_reports = []
for student in students:
    for course in courses:
        final_score = np.clip(np.random.normal(78, 12), 0, 100)
        final_reports.append({
            'student_id': student['student_id'],
            'course': course,
            'final_report_score': final_score
        })
final_df = pd.DataFrame(final_reports)

# 保存为CSV
students_df.to_csv('students.csv', index=False, encoding='utf-8-sig')
behavior_df.to_csv('learning_behavior.csv', index=False, encoding='utf-8-sig')
final_df.to_csv('final_reports.csv', index=False, encoding='utf-8-sig')

print("数据生成完成！")