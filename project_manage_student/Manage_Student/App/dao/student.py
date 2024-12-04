from wtforms.validators import email

from App import db
from App.model import Student, Profile


# def add_list_student(list_data, staff_id):
#     # tạo đối tượng profile
#     for profile in list_data:
#         p = Profile(name=profile['name'], email=profile['email'])
#         db.session.add(p)
#     db.session.commit()
#
#     # tạo đối tượng student
#     for data in list_data:
#         p = Profile.query.filter(Profile.email.__eq__(data['email'])).first()
#         student = Student(id=p.id, staff_id=staff_id)
#         db.session.add(student)
#     db.session.commit()


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


def load_students(user_id):
    return Student.query.filter(Student.id.__eq__(user_id))
