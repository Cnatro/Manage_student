import pdb

from wtforms.validators import email

from App import db
from sqlalchemy import delete
from App.model import Student, Profile, StudentClass, Score,Exam
from App.dao import exam,classes


def add_list_student(list_data, staff_id):
    for p in list_data:
        create_student(name=p['name'],
                       birthday=None,
                       gender=None,
                       address=None,
                       email=p['email'],
                       number_phone=None,
                       staff_id=staff_id)


def create_student(name, birthday, gender, address ,email, number_phone,staff_id):
    p = Profile(name=name,
                birthday=birthday,
                gender=gender,
                address=address,
                email=email,
                number_phone=number_phone)
    db.session.add(p)
    db.session.commit()

    st = Student(id=p.id, staff_id=staff_id)
    db.session.add(st)
    db.session.commit()


def del_student(student_id):
    exam_ = exam.get_exam_by_student_id(student_id=student_id)
    if exam_:
        exam_ids = [ex.id for ex in exam_]
        query_del_score = delete(Score).where(Score.exam_id.in_(exam_ids))
        query_del_exam = delete(Exam).where(Exam.student_id.__eq__(student_id))


        db.session.execute(query_del_score)
        db.session.execute(query_del_exam)

    query_del_student_class = delete(StudentClass).where(StudentClass.student_id.__eq__(student_id))
    query_del_student = delete(Student).where(Student.id.__eq__(student_id))
    query_del_profile = delete(Profile).where(Profile.id.__eq__(student_id))

    db.session.execute(query_del_student_class)
    db.session.execute(query_del_student)
    db.session.execute(query_del_profile)

    db.session.commit()
    classes.count_student_of_class()

