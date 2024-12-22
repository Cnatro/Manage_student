from datetime import datetime

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
                    TeacherSubject.teacher_id.__eq__(teacher_id),
                    Semester.year.__eq__(datetime.now().year)).all())


def get_plan(class_id,teacher_id,semester_id,subject_id):
    return (db.session.query(TeacherPlan)
            .join(Class, Class.id.__eq__(TeacherPlan.class_id))
            .join(TeacherSubject, TeacherSubject.id.__eq__(TeacherPlan.teacher_subject_id))
            .join(Semester, Semester.id == TeacherPlan.semester_id)
            .join(Subject, Subject.id == TeacherSubject.subject_id)
            .filter(TeacherPlan.class_id.__eq__(class_id),
                    TeacherPlan.semester_id.__eq__(semester_id),
                    TeacherSubject.teacher_id.__eq__(teacher_id),
                    TeacherSubject.subject_id.__eq__(subject_id)).first())


def get_teaching_plan_by_id(teacher_plan_id):
    return TeacherPlan.query.filter(TeacherPlan.id.__eq__(teacher_plan_id)).first()


if __name__ == '__main__':
    with app.app_context():
       print(get_plan(class_id=1,subject_id=1,semester_id=7,teacher_id=4))
