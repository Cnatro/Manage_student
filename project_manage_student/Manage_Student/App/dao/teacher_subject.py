from App.model import Subject,TeacherSubject

def get_subjects_by_grade(grade):
    return Subject.query.filter(Subject.grade.__eq__(grade)).all()


def get_all_teacher_by_subject(subject_id):
    return TeacherSubject.query.filter(TeacherSubject.subject_id.__eq__(subject_id)).all()