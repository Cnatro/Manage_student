from App.model import Class,StudentClass
from App import db
from sqlalchemy import func

def get_list_class(grade=None):
    query = Class.query
    if grade:
        return query.filter(Class.grade.__eq__(grade)).all()
    return query.all()


def get_list_class_less_quantity(quantity_student_max):
    return Class.query.filter(Class.quantity_student < quantity_student_max).all()


def get_class_by_id(class_id):
    return Class.query.filter(Class.id.__eq__(class_id)).first()


def count_student_of_class():
    classes = Class.query.all()
    for c in classes:
        c.quantity_student = (db.session.query(func.count(StudentClass.class_id))
                              .filter(StudentClass.class_id.__eq__(c.id)).scalar())
        db.session.add(c)
    db.session.commit()