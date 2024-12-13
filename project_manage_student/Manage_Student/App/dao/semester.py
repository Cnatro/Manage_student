from App.model import Semester

def get_all_semester():
    return Semester.query.order_by(Semester.id.desc()).all()


def unique_semester(semesters):
    # loại bỏ được kí tu trùng k giữ thứ tự
    # unique_dt = { s.year for s in semesters }
    # giữ được thứ tự
    unique_dt = list(dict.fromkeys(s.year for s in semesters))
    return unique_dt


def get_semester_by_year(year_):
    return Semester.query.filter(Semester.year.__eq__(year_)).all()