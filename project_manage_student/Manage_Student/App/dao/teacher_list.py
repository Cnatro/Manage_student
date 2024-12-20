from App.model import TeacherPlan, Class, Subject, TeacherSubject,Semester
from App import db, app


def get_class_by_teacher_id(teacher_id):
    return (db.session.query(Class)
            .join(TeacherPlan, TeacherPlan.class_id.__eq__(Class.id))
            .join(TeacherSubject, TeacherSubject.id.__eq__(TeacherPlan.teacher_subject_id))
            .join(Semester, Semester.id == TeacherPlan.semester_id)
            .join(Subject, Subject.id == TeacherSubject.subject_id)
            .filter(TeacherSubject.teacher_id.__eq__(teacher_id)).all())

def get_plan_by_class_id(class_id,teacher_id):
    return (db.session.query(TeacherPlan)
            .join(Class, Class.id.__eq__(TeacherPlan.class_id))
            .join(TeacherSubject, TeacherSubject.id.__eq__(TeacherPlan.teacher_subject_id))
            .join(Semester, Semester.id == TeacherPlan.semester_id)
            .join(Subject, Subject.id == TeacherSubject.subject_id)
            .filter(TeacherPlan.class_id.__eq__(class_id),
                    TeacherSubject.teacher_id.__eq__(teacher_id)).all())


if __name__ == '__main__':
    with app.app_context():
       print(get_plan_by_class_id(class_id=1,teacher_id=4))
