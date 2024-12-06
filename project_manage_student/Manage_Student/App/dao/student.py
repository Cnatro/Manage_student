from wtforms.validators import email

from App import db
from App.model import Student, Profile


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

