from App.model import Class

def get_list_class(grade=None):
    query = Class.query
    if grade:
        return query.filter(Class.grade.__eq__(grade)).all()
    return query.all()