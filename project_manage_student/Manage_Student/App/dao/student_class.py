import random

from sqlalchemy import func

from App.model import Student, Class, Grade, StudentClass, User, UserRole
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