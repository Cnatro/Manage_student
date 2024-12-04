from App.model import TeacherPlan, TeacherSubject, Class,Semester,Student
from App import db
from sqlalchemy import distinct


# # #lay du lieu ds mon hoc
# def get_list_subject_by_teacher_id(teacher_id):
#     return TeacherPlan.query.filter(TeacherPlan.teacher_subject_id.teacher_id.__eq__(teacher_id).all()
# #
# #
def get_teacher_plan_by_id(teacher_id):
    return (db.session.query(TeacherPlan)
            .join(TeacherSubject)
            .join(Class)
            .join(Student)
            .join(Semester)
            .filter(TeacherSubject.teacher_id.__eq__(teacher_id))).all()

# def get_teacher_plan_by_id(teacher_id):
#     # Lấy dữ liệu từ bảng TeacherPlan
#     query = (db.session.query(TeacherPlan)
#              .join(TeacherSubject)
#              .join(Class)
#              .join(Semester)
#              .filter(TeacherSubject.teacher_id.__eq__(teacher_id)))
#
#     # Loại bỏ trùng lặp year
#     unique_years = set()
#     unique_results = []
#
#     for plan in query.all():
#         if plan.semesters.year not in unique_years:
#             unique_results.append(plan)
#             unique_years.add(plan.semesters.year)
#
#     return unique_results
