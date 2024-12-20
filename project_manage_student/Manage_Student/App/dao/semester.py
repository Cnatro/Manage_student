from App.model import Semester

# def get_all_semester():
#     return Semester.query.order_by(Semester.id.desc()).all()


# def unique_semester(semesters):
#     grouped_data = {}
#     for s in semesters:
#         if s.year not in grouped_data:
#             grouped_data[s.year] = []
#         grouped_data[s.year].append({
#             "semester_name": s.name,
#             "semester_id": s.id
#         })
#     return grouped_data


def get_semester_by_year(year_):
    return Semester.query.filter(Semester.year.__eq__(year_)).all()