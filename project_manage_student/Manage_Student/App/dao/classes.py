from App.model import Class

def get_list_class():
    return Class.query.all()