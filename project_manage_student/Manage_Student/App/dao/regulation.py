from App.model import *


def get_regulations():
    return Regulation.query.all()


def get_regulation_by_name(type_):
    return db.session.query(Regulation).filter(Regulation.type.__eq__(type_)).first()


if __name__ == '__main__':
    with app.app_context():
        print(get_regulation_by_name('Quantity_student').max)