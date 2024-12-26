import pdb

from sqlalchemy import case, func

from App import db
from App.model import Subject, TeacherSubject, Grade, StudentClass, Student, Score, Exam, TeacherPlan
from App.dao import teacher_list, classes


def get_subjects_by_grade(grade):
    return Subject.query.filter(Subject.grade.__eq__(grade)).all()


def get_all_teacher_by_subject(subject_id):
    return TeacherSubject.query.filter(TeacherSubject.subject_id.__eq__(subject_id)).all()


def get_subject_by_id(subject_id):
    return Subject.query.filter(Subject.id.__eq__(subject_id)).first()


def get_avg_score_of_subject(semester_id, subject_id):
    student_dtb = get_student_avg_in_grade(semester_id=semester_id, subject_id=subject_id)

    result = (db.session.query(StudentClass.class_id, func.avg(student_dtb.c.dtb))
              .join(student_dtb, student_dtb.c.id.__eq__(StudentClass.student_id))
              .order_by(StudentClass.class_id)
              .group_by(StudentClass.class_id)).all()
    return result


def student_classification(semester_id, subject_id):
    # ds điểm trung bình của student (id,dtb)
    student_dtb = get_student_avg_in_grade(semester_id=semester_id, subject_id=subject_id)
    # count student dạt or rot của 1 lớp
    student_final = db.session.query(student_dtb,
                                     case((student_dtb.c.dtb >= 5, 'Đậu'), (student_dtb.c.dtb < 5, 'Rớt')).label(
                                         'ket_qua')).subquery()
    result = (db.session.query(StudentClass.class_id,
                               func.count(
                                   case((student_final.c.ket_qua.__eq__('Đậu'), 1))
                               ))
              .join(student_final, student_final.c.id.__eq__(StudentClass.student_id))
              .order_by(StudentClass.class_id)
              .group_by(StudentClass.class_id).all())
    return result


def get_classification_in_subject(semester_id, subject_id):
    student_dtb = get_student_avg_in_grade(semester_id=semester_id, subject_id=subject_id)

    result = db.session.query(func.sum(case((student_dtb.c.dtb >= 8 , 1))),
                              func.sum(case((student_dtb.c.dtb.between(6.5, 7.99999999),1))),
                              func.sum(case((student_dtb.c.dtb.between(5,6.49999999),1)) ),
                              func.sum(case((student_dtb.c.dtb < 5 ,1)))).all()
    return result


def get_student_avg_in_grade(semester_id, subject_id):
    return (db.session.query(Student.id.label('id'),
                             (
                                     func.sum(case(
                                         (Score.type_exam.__eq__('EXAM_15P'), Score.value * 1),
                                         (Score.type_exam.__eq__('EXAM_45P'), Score.value * 2),
                                         (Score.type_exam.__eq__('FINAL_EXAM'), Score.value * 3)
                                     )) /
                                     func.sum(case(
                                         (Score.type_exam.__eq__('EXAM_15P'), 1),
                                         (Score.type_exam.__eq__('EXAM_45P'), 2),
                                         (Score.type_exam.__eq__('FINAL_EXAM'), 3))
                                     )
                             ).label('dtb'))
            .join(Exam, Exam.student_id.__eq__(Student.id))
            .join(Score, Score.exam_id.__eq__(Exam.id))
            .join(TeacherPlan, TeacherPlan.id.__eq__(Exam.teacher_plan_id))
            .join(TeacherSubject, TeacherSubject.id.__eq__(TeacherPlan.teacher_subject_id))
            .filter(TeacherSubject.subject_id.__eq__(subject_id))
            .filter(TeacherPlan.semester_id.__eq__(semester_id))
            .group_by(Student.id).subquery())
