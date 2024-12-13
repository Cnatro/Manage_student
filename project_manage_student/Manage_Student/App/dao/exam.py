from App.model import Exam, Class, TeacherPlan, Student, Score, StudentClass
from App import db

def get_info_old_students(grade_):
    # - lấy danh sách học sinh và các điểm của nó trong khối đó
    return (db.session.query(Exam)
            .join(Score, Score.exam_id == Exam.id)
            .join(Student,Student.id == Exam.student_id)
            .join(StudentClass,StudentClass.student_id == Student.id)
            .join(Class, Class.id == StudentClass.class_id)
            .filter(Class.grade.__eq__(grade_))
            .all()
            )


def get_info_students_for_excel(old_students):
    data = {}
    if old_students:
        data =[
            {
                'Fullname':st.student.profile.name,
                'Gender':st.student.profile.gender,
                'Birthday':st.student.profile.birthday,
                # 'Scores':st.exam.scores.type_exam,
                'Scores': 10,
                'Subject':st.teacher_plans.teacher_subjects.subjects.name,
                'Class':st.teacher_plans.classes.name,
                'Grade':st.teacher_plans.classes.grade.name,
                'Semester':st.teacher_plans.semester.name.name,
                'learn_year':st.teacher_plans.semester.year
            }
            for st in old_students
        ]
    return data
