from datetime import datetime
from itertools import groupby

from App.model import TeacherPlan, Class, Subject, TeacherSubject, Semester,Profile, Student, Score, Exam, StudentClass
from App import db, app
from sqlalchemy.sql import func,case

def get_class_by_teacher_id(teacher_id):
    return (db.session.query(Class)
            .join(TeacherPlan, TeacherPlan.class_id.__eq__(Class.id))
            .join(TeacherSubject, TeacherSubject.id.__eq__(TeacherPlan.teacher_subject_id))
            .join(Semester, Semester.id == TeacherPlan.semester_id)
            .join(Subject, Subject.id == TeacherSubject.subject_id)
            .filter(TeacherSubject.teacher_id.__eq__(teacher_id)).all())


def get_plan_by_class_id(class_id,teacher_id):
    return (db.session.query(TeacherPlan)
            .join(Class, Class.id.__eq__(TeacherPlan.class_id))
            .join(TeacherSubject, TeacherSubject.id.__eq__(TeacherPlan.teacher_subject_id))
            .join(Semester, Semester.id == TeacherPlan.semester_id)
            .join(Subject, Subject.id == TeacherSubject.subject_id)
            .filter(TeacherPlan.class_id.__eq__(class_id),
                    TeacherSubject.teacher_id.__eq__(teacher_id),
                    Semester.year.__eq__(datetime.now().year)).all())


def get_plan(class_id,teacher_id,semester_id,subject_id):
    return (db.session.query(TeacherPlan)
            .join(Class, Class.id.__eq__(TeacherPlan.class_id))
            .join(TeacherSubject, TeacherSubject.id.__eq__(TeacherPlan.teacher_subject_id))
            .join(Semester, Semester.id == TeacherPlan.semester_id)
            .join(Subject, Subject.id == TeacherSubject.subject_id)
            .filter(TeacherPlan.class_id.__eq__(class_id),
                    TeacherPlan.semester_id.__eq__(semester_id),
                    TeacherSubject.teacher_id.__eq__(teacher_id),
                    TeacherSubject.subject_id.__eq__(subject_id)).first())


def get_teaching_plan_by_id(teacher_plan_id):
    return TeacherPlan.query.filter(TeacherPlan.id.__eq__(teacher_plan_id)).first()

def get_final_exam_scores(semester_id, subject_id, class_id):
    return (db.session.query(Student.id)
            .join(Exam, Exam.student_id == Student.id)
            .join(Score, Score.exam_id == Exam.id)
            .join(TeacherPlan, TeacherPlan.id == Exam.teacher_plan_id)
            .join(TeacherSubject, TeacherSubject.id == TeacherPlan.teacher_subject_id)
            .filter(
                TeacherPlan.semester_id == semester_id,
                TeacherSubject.subject_id == subject_id,
                TeacherPlan.class_id == class_id,
                Score.type_exam == "FINAL_EXAM"
            ).all())

def average_score(semester_id, subject_id, class_id):
    average = db.session.query(
        Student.id,
        Profile.name,
        func.sum(case(
            (Score.type_exam == "EXAM_15P", Score.value * 1),
            (Score.type_exam == "EXAM_45P", Score.value * 2),
            (Score.type_exam == "FINAL_EXAM", Score.value * 3)
        )) / func.sum(case(
            (Score.type_exam == "EXAM_15P", 1),
            (Score.type_exam == "EXAM_45P", 2),
            (Score.type_exam == "FINAL_EXAM", 3)
        )).label('average_score')
        ).select_from(Student
        ).join(Profile, Profile.id == Student.id
        ).join(StudentClass, StudentClass.student_id == Student.id
        ).join(Exam, Exam.student_id == Student.id
        ).join(Score, Score.exam_id == Exam.id
        ).join(TeacherPlan, TeacherPlan.id == Exam.teacher_plan_id
        ).join(TeacherSubject,TeacherSubject.id == TeacherPlan.teacher_subject_id
        ).filter(
            StudentClass.class_id == class_id,
            TeacherPlan.teacher_subjects.has(subject_id=subject_id),
            TeacherPlan.semester_id == semester_id,
        ).group_by(Student.id, Profile.name).all()
    return  average

def get_semesters_by_year(year):
    return (db.session.query(Semester)
            .filter(Semester.year.__eq__(year))
            .all())

def init_student_scores(teach_plan):
    """Khởi tạo dictionary lưu điểm cho học sinh."""
    student_scores = {}
    for student_class in teach_plan.classes.student_class:
        student_scores[student_class.students.id] = {'HK1': None, 'HK2': None}
    return student_scores


def update_scores(semester, averages, student_final_check, student_scores):
    """Cập nhật điểm trung bình cho từng học sinh."""
    for student_id, name, avg_score in averages:
        if student_id in student_final_check and avg_score is not None:
            semester_name = f"{semester.name.name}"
            student_scores[student_id][semester_name] = round(float(avg_score), 2)


def process_scores(semester, teach_plan, student_scores):
    """Xử lý điểm trung bình cho từng học kỳ."""
    # Lấy danh sách học sinh có điểm final exam
    students_final = get_final_exam_scores(
        semester.id,
        teach_plan.teacher_subjects.subject_id,
        teach_plan.class_id
    )
    student_final_check = {student.id for student in students_final}

    # Nếu có học sinh có điểm final exam, tính điểm trung bình
    if student_final_check:
        averages = average_score(
            semester.id,
            teach_plan.teacher_subjects.subject_id,
            teach_plan.class_id
        )
        update_scores(semester, averages, student_final_check, student_scores)

def get_average_score_for_excel(students):
    data = {}
    if students:
        data =[
            {
                'Fullname':st.student.profile.name,
                'Class': st.teacher_plans.classes.name,
            }
            for st in students
        ]

        score =[
            {

            }
        ]
    return data



if __name__ == '__main__':
    with app.app_context():
        print(average_score(subject_id=1,semester_id=5,class_id=1))
