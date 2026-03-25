import pandas as pd
import numpy as np

# 读取数据
students = pd.read_csv('students.csv')
behavior = pd.read_csv('learning_behavior.csv')
final = pd.read_csv('final_reports.csv')
behavior['date'] = pd.to_datetime(behavior['date'])


def extract_features(student_id, course):
    stu_course = behavior[(behavior['student_id'] == student_id) & (behavior['course'] == course)]

    # 1. 知识掌握度：测验和作业的平均分
    exam_hw = stu_course[stu_course['activity_type'].isin(['测验', '作业提交'])]
    knowledge_mastery = exam_hw['score'].mean() if len(exam_hw) > 0 else np.nan

    # 2. 实验操作能力：综合得分
    lab_ops = stu_course[stu_course['activity_type'] == '实验操作']
    if len(lab_ops) > 0:
        lab_score_mean = lab_ops['score'].mean()
        error_mean = lab_ops['error_count'].mean() if 'error_count' in lab_ops else 0
        time_mean = lab_ops['time_spent_min'].mean() if 'time_spent_min' in lab_ops else 45
        time_penalty = max(0, 1 - abs(time_mean - 45) / 45) if not pd.isna(time_mean) else 1
        error_penalty = max(0, 1 - error_mean / 5) if not pd.isna(error_mean) else 1
        lab_ability = lab_score_mean / 100 * (0.5 * time_penalty + 0.5 * error_penalty) * 100
    else:
        lab_ability = np.nan

    # 3. 学习习惯：时间段偏好 + 活动频率
    if not stu_course.empty:
        hours = stu_course['date'].dt.hour
        morning = sum((hours >= 6) & (hours <= 11))
        afternoon = sum((hours >= 12) & (hours <= 17))
        evening = sum((hours >= 18) & (hours <= 23))
        time_pref = 'morning' if morning >= max(afternoon, evening) else \
            'afternoon' if afternoon >= evening else 'evening'
        # 每月平均活动次数
        days_span = (behavior['date'].max() - behavior['date'].min()).days
        months = max(1, days_span / 30)
        activity_freq = len(stu_course) / months
    else:
        time_pref = 'unknown'
        activity_freq = 0

    final_score = final[(final['student_id'] == student_id) & (final['course'] == course)]['final_report_score'].values
    final_score = final_score[0] if len(final_score) > 0 else np.nan

    return {
        'student_id': student_id,
        'course': course,
        'knowledge_mastery': round(knowledge_mastery, 1) if not pd.isna(knowledge_mastery) else None,
        'lab_ability': round(lab_ability, 1) if not pd.isna(lab_ability) else None,
        'activity_freq': round(activity_freq, 1),
        'time_preference': time_pref,
        'final_report_score': round(final_score, 1) if not pd.isna(final_score) else None
    }


all_courses = behavior['course'].unique()
all_students = students['student_id'].unique()

features = []
for sid in all_students:
    for c in all_courses:
        features.append(extract_features(sid, c))

features_df = pd.DataFrame(features)
features_df.to_csv('student_course_features.csv', index=False, encoding='utf-8-sig')
print("特征提取完成，保存至 student_course_features.csv")