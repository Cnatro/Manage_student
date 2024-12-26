import random
from sqlalchemy import delete

from App.model import Student, Class, Grade, StudentClass, User, UserRole, Score, Exam, TeacherPlan, Profile
from App import db
from App.dao import classes


def auto_create_class(quantity_student):
    global class_
    # outerjoin = leftJoin
    students = get_list_student_no_class()

    teacher_masters = User.query.filter(User.user_role.__eq__(UserRole.TEACHER)).all()
    count = 0
    class_number = 1

    for student in students:
        if count == 0 or count == quantity_student:
            class_name = f"10A{class_number}"
            class_number += 1  # Tăng số thứ tự lớp
            teacher_master = random.choice(teacher_masters)

            class_ = Class(name=class_name, grade=Grade.K10, teacher_id=teacher_master.id)
            db.session.add(class_)
            db.session.commit()
            count = 0

        count = count + 1
        student_class = StudentClass(student_id=student.id, class_id=class_.id)
        db.session.add(student_class)
    db.session.commit()
    # cập nhật số lượng họp sinh trong lớp
    classes.count_student_of_class()


def get_list_student(class_id=None, value_name=None):
    query = StudentClass.query
    if class_id and value_name:
        return (query.join(Profile, Profile.id == StudentClass.student_id)
                .filter(Profile.name.contains(value_name), StudentClass.class_id.__eq__(class_id)).all())
    if class_id:
        return query.filter(StudentClass.class_id.__eq__(class_id)).all()
    if value_name:
        return (query.join(Profile, Profile.id == StudentClass.student_id)
                .filter(Profile.name.contains(value_name)).all())
    return query.all()


def get_list_student_no_class():
    query = (db.session.query(Student).outerjoin(StudentClass, Student.id.__eq__(StudentClass.student_id))
             .filter(StudentClass.student_id.__eq__(None)).all())
    return query


def load_students():
    return StudentClass.query.all()


def change_student_to_class(class_id, student_ids):
    student_ids = [int(x) for x in student_ids]

    students = StudentClass.query.filter(StudentClass.student_id.in_(student_ids)).all()
    for st in students:
        st.class_id = class_id
        db.session.add(st)
    db.session.commit()
    classes.count_student_of_class()


def update_class(grade, old_students):
    count = 1
    grade = grade + 1

    # lấy ds class_id của hs cũ
    classes_update = {ex.teacher_plans.classes.id for ex in old_students}
    # lấy class
    class_old = Class.query.filter(Class.id.in_(classes_update)).all()
    # update
    for c in class_old:
        c.name = f'{grade}A{count}'
        c.grade = Grade(grade)

        count = count + 1
        db.session.add(c)

    db.session.commit()


def reset_info_students(old_students):
    student_ids = [ex.student_id for ex in old_students]
    exam_ids = [ex.id for ex in old_students]
    class_ids = {ex.teacher_plans.classes.id for ex in old_students}

    query_score = delete(Score).where(Score.exam_id.in_(exam_ids))
    query_exam = delete(Exam).where(Exam.student_id.in_(student_ids))
    query_teacher_plan = delete(TeacherPlan).where(TeacherPlan.class_id.in_(class_ids))

    db.session.execute(query_score)
    db.session.execute(query_exam)
    db.session.execute(query_teacher_plan)

    # print("Deleted rows in Score:", result_score.rowcount)
    # print("Deleted rows in Exam:", result_exam.rowcount)
    # print("Deleted rows in TeacherPlan:", result_teacher_plan.rowcount)
    db.session.commit()


def add_student_class(student_ids, class_id):
    for id in student_ids:
        st = StudentClass(student_id=id, class_id=class_id)
        db.session.add(st)
    db.session.commit()
    classes.count_student_of_class()


def get_student_by_id(student_id):
    return StudentClass.query.filter(StudentClass.student_id.__eq__(student_id)).first()
