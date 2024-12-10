from App.model import Class, Student
from App import db

def get_list_class(grade=None):
    query = Class.query
    if grade:
        return query.filter(Class.grade.__eq__(grade)).all()
    return query.all()

def get_list_class_less_quantity(quantity_student_max):
    return Class.query.filter(Class.quantity_student < quantity_student_max).all()


