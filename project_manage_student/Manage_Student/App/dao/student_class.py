import random
from sqlalchemy import delete
from sqlalchemy import func

from App.model import Student, Class, Grade, StudentClass, User, UserRole, Score, Exam, TeacherPlan
from App import db


def auto_create_class(quantity_student):
    global class_
    # outerjoin = leftJoin
    students = (db.session.query(Student).outerjoin(StudentClass, Student.id.__eq__(StudentClass.student_id))
                .filter(StudentClass.student_id.__eq__(None)).all())

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
    count_student_of_class()


def get_list_student_by_class_id(class_id=None):
    query = StudentClass.query
    if class_id:
        return query.filter(StudentClass.class_id.__eq__(class_id)).all()
    return query.all()


def load_students():
    return StudentClass.query.all()


def count_student_of_class():
    classes = Class.query.all()
    for c in classes:
        c.quantity_student = (db.session.query(func.count(StudentClass.class_id))
                                      .filter(StudentClass.class_id.__eq__(c.id)).scalar())
        db.session.add(c)
    db.session.commit()


def change_student_to_class(class_id, student_ids):
    student_ids = [int(x) for x in student_ids]

    students = StudentClass.query.filter(StudentClass.student_id.in_(student_ids)).all()
    for st in students:
        st.class_id = class_id
        db.session.add(st)
    db.session.commit()
    count_student_of_class()


def update_class(grade,old_students):
    count = 1
    grade = grade + 1

    # lấy ds class_id của hs cũ
    classes_update = {ex.teacher_plans.classes.id for ex in old_students}
    #lấy class
    class_old = Class.query.filter(Class.id.in_(classes_update)).all()
    # update
    for c in class_old:
        c.name = f'{grade}A{count}'
        c.grade = Grade(grade)

        count = count + 1
        db.session.add(c)

    db.session.commit()


def reset_info_students(old_students):
    student_ids = [ ex.student_id for ex in old_students ]
    exam_ids = [ ex.id for ex in old_students ]
    class_ids = { ex.teacher_plans.classes.id for ex in old_students }

    print(student_ids)
    print(exam_ids)
    print(class_ids)
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

