from sqlalchemy import func

from App import db
from App.model import Subject, Semester, Grade, StudentClass, Score, Class, Exam


def get_subjects():
    """Lấy danh sách môn học, loại bỏ môn trùng lặp theo tên và lớp."""
    return db.session.query(Subject).distinct(Subject.name).all()


def get_semesters():
    """Trả về danh sách mặc định các học kỳ: HK1, HK2, HK3."""
    return [{'id': 1, 'name': 'HK1'}, {'id': 2, 'name': 'HK2'}, {'id': 3, 'name': 'HK3'}]

def get_years():
    """Lấy danh sách các năm học."""
    return db.session.query(Semester.year).distinct().all()

def get_grades():
    """Lấy danh sách khối lớp."""
    return db.session.query(Grade).all()

def get_subjects_by_grade():
    subjects = db.session.query(Subject).distinct(Subject.name).all()
    subjects_by_grade = {}
    for subject in subjects:
        if subject.grade not in subjects_by_grade:
            subjects_by_grade[subject.grade] = []
        subjects_by_grade[subject.grade].append(subject)
    return subjects_by_grade

def get_report_data(grade, semester, year):
    # Sử dụng các bảng và trường đúng để truy vấn dữ liệu
    return db.session.query(
        Class.name.label("class_name"),
        func.count(StudentClass.student_id).filter(Score.value >= 5).label("students_passed"),  # Sửa 'score' thành 'value'
        func.avg(Score.value).label("average_score")  # Sửa 'score' thành 'value'
    ).join(
        StudentClass, StudentClass.class_id == Class.id  # Kết nối StudentClass với Class
    ).join(
        Exam, Exam.student_id == StudentClass.student_id  # Kết nối Exam với Student thông qua student_id
    ).join(
        Score, Score.exam_id == Exam.id  # Kết nối Score với Exam
    ).join(
        Semester, Semester.year == year  # Kết nối Semester với năm học
    ).filter(
        Class.grade == grade,  # Bộ lọc theo lớp học
        Semester.name == semester  # Bộ lọc theo học kỳ
    ).group_by(Class.id).all()  # Nhóm kết quả theo lớp học



