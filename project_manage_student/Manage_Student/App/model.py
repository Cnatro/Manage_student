import enum
import hashlib

from App import app,db
from sqlalchemy import Integer, Column, String, ForeignKey, Float, DateTime, Boolean, Text, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import func
from flask_login import UserMixin


class UserRole(enum.Enum):
    TEACHER = 1
    STAFF = 2
    ADMIN = 3


class Grade(enum.Enum):
    K10 = 10
    K11 = 11
    K12 = 12


class SemesterName(enum.Enum):
    HK1 = 1
    HK2 = 2


class Profile(db.Model):
    id = Column(Integer,autoincrement=True,primary_key=True)
    name = Column(String(50))
    birthday = Column(DateTime)
    gender = Column(Boolean)
    address = Column(Text)
    email = Column(String(50),unique=True,nullable=False)
    number_phone = Column(String(10),unique=True)


class User(db.Model,UserMixin):
    id = Column(Integer,ForeignKey(Profile.id),primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole))
    create_day = Column(DateTime,default=func.now())
    last_login = Column(DateTime)

    profile = relationship('Profile',backref='User',lazy=True)
    # staff
    staff_students = relationship('Student',backref='User',lazy=True)
    # teacher
    teach_classes = relationship('Class',backref='User',lazy=True)


class Student(db.Model):
    id = Column(Integer,ForeignKey(Profile.id), primary_key=True)
    status_payment = Column(Boolean,default=False)

    staff_id = Column(Integer, ForeignKey(User.id),nullable=False)

    profile = relationship('Profile',backref='Student',lazy=True)


class Class(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(20),nullable=False)
    quantity_student = Column(Integer)
    grade = Column(Enum(Grade))

    teacher_id = Column(Integer,ForeignKey(User.id),nullable=False)


class Subject(db.Model):
    id = Column(Integer, autoincrement=True, primary_key= True)
    name = Column(String(50))
    grade = Column(Enum(Grade))
    number_of_15p = Column(Integer,default=1)
    number_of_45p = Column(Integer,default=1)


class Semester(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Enum(SemesterName))
    year = Column(DateTime)


class StudentClass(db.Model):
    id = Column(Integer,autoincrement=True, primary_key=True)

    student_id = Column(Integer,ForeignKey(Student.id), nullable=False)
    class_id = Column(Integer,ForeignKey(Class.id),nullable=False)

    students = relationship('Student',backref='StudentClass',lazy=True)
    class_ = relationship('Class',backref='StudentClass',lazy=True)


class StaffClass(db.Model):
    id = Column(Integer,autoincrement=True,primary_key=True)

    staff_id = Column(Integer,ForeignKey(User.id), nullable=False)
    class_id = Column(Integer,ForeignKey(Class.id), nullable = False)

    staff = relationship('User',backref='StaffClass',lazy=True)
    class_ = relationship('Class',backref='StaffClass',lazy=True)


class TeacherSubject(db.Model):
    id = Column(Integer, autoincrement= True, primary_key=True)

    teacher_id = Column(Integer, ForeignKey(User.id), nullable= False)
    subject_id  = Column(Integer, ForeignKey(Subject.id), nullable= False)

    teacher = relationship('User',backref='TeacherSubject',lazy=True)
    subjects = relationship('Subject',backref='TeacherSubject',lazy=True)

class TeacherPlan(db.Model):
    id = Column(Integer, autoincrement= True, primary_key=True)

    teacher_subject_id = Column(Integer, ForeignKey(TeacherSubject.id), nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable= False)
    semester_id = Column(Integer, ForeignKey(Semester.id ), nullable= False)

    teacher_subjects = relationship('TeacherSubject',backref='TeacherPlan',lazy=True)
    semester = relationship('Semester',backref='TeacherPlan',lazy=True)
    classes = relationship('Class',backref='TeacherPlan',lazy=True)


class Exam(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True)

    teacher_plan_id = Column(Integer,ForeignKey(TeacherPlan.id),nullable=False)
    student_id = Column(Integer,ForeignKey(Student.id),nullable=False)

    teacher_plans = relationship('TeacherPlan',backref='Exam',lazy=True)
    scores = relationship('Score',backref='Exam',lazy=True)


class Score(db.Model):
    id = Column(Integer,autoincrement=True, primary_key=True)
    type_exam = Column(String(20), nullable=False)
    value = Column(Float,nullable=False)
    count_exam = Column(Integer)

    exam_id = Column(Integer,ForeignKey(Exam.id),nullable=False)

    __table_args__ = (
        CheckConstraint('value >= 0', name='check_value_min'),
        CheckConstraint('value <= 10', name='check_value_max'),
    )


class Regulation(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True)
    type = Column(String(50))
    regulation_name = Column(String(100))
    min = Column(Integer)
    max = Column(Integer)

    admin_id = Column(Integer, ForeignKey(User.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()

        #create user
        profile_1 = Profile(name='Nguyễn Hoàng Long Nhật',email='cnatro23@gmail.com')
        profile_2 = Profile(name='Trần Lê Nhân', email='nhantran.011004@gmail.com')
        profile_3 = Profile(name='Hồ Ngọc Thái', email='ngocthai@gmail.com')
        # db.session.add_all([profile_1,profile_2,profile_3])
        # db.session.commit()

        #create account
        admin = User(id=profile_1.id,username="Cnatro",password=str(hashlib.md5('Admin123@'.encode('utf-8')).hexdigest()),user_role=UserRole.STAFF)
        acc2 = User(id=profile_2.id,username="NhanTran",password=str(hashlib.md5('Nhan123@'.encode('utf-8')).hexdigest()), user_role=UserRole.TEACHER)
        acc3 = User(id=profile_3.id,username="NgocThai",password=str(hashlib.md5('Thai123@'.encode('utf-8')).hexdigest()), user_role=UserRole.ADMIN)

        # db.session.add_all([admin,acc2,acc3])
        # db.session.commit()

        # create teacher
        p4 = Profile(name="Giáo viên toán 10 11 12", email="GV4@gmail.com")
        p5 = Profile(name="Giáo viên lý 10 11 12", email="GV5@gmail.com")
        p6 = Profile(name="Giáo viên hóa 10 11 12", email="GV6@gmail.com")
        p7 = Profile(name="Giáo viên sinh 10 11 12", email="GV7@gmail.com")
        p8 = Profile(name="Giáo viên văn 10 11 12" ,email="GV8@gmail.com")
        p9 = Profile(name="Giáo viên anh 10 11 12", email="GV9@gmail.com")

        # db.session.add_all([p4,p5,p6,p7,p8,p9])
        # db.session.commit()

        teacher4 = User(id=p4.id,username="Gv4",password=str(hashlib.md5('Gv4123@'.encode('utf-8')).hexdigest()),
                    user_role=UserRole.TEACHER)
        teacher5 = User(id=p5.id, username="Gv5", password=str(hashlib.md5('Gv5123@'.encode('utf-8')).hexdigest()),
                    user_role=UserRole.TEACHER)
        teacher6 = User(id=p6.id, username="Gv6", password=str(hashlib.md5('Gv6123@'.encode('utf-8')).hexdigest()),
                    user_role=UserRole.TEACHER)
        teacher7 = User(id=p7.id, username="Gv7", password=str(hashlib.md5('Gv7123@'.encode('utf-8')).hexdigest()),
                    user_role=UserRole.TEACHER)
        teacher8 = User(id=p8.id, username="Gv8", password=str(hashlib.md5('Gv8123@'.encode('utf-8')).hexdigest()),
                    user_role=UserRole.TEACHER)
        teacher9 = User(id=p9.id, username="Gv9", password=str(hashlib.md5('Gv9123@'.encode('utf-8')).hexdigest()),
                    user_role=UserRole.TEACHER)

        # db.session.add_all([teacher4, teacher5, teacher6, teacher7, teacher8, teacher9])
        # db.session.commit()

        #create subject
        subjects = [
            Subject(name="Toán", grade=Grade.K10, number_of_15p=3,number_of_45p=3),
            Subject(name="Lý", grade=Grade.K10, number_of_15p=3, number_of_45p=3),
            Subject(name="Hóa", grade=Grade.K10, number_of_15p=3, number_of_45p=3),
            Subject(name="Sinh", grade=Grade.K10, number_of_15p=3, number_of_45p=3),
            Subject(name="Văn", grade=Grade.K10, number_of_15p=3, number_of_45p=3),
            Subject(name="Anh", grade=Grade.K10, number_of_15p=3, number_of_45p=3),

            Subject(name="Toán", grade=Grade.K11, number_of_15p=3, number_of_45p=3),
            Subject(name="Lý", grade=Grade.K11, number_of_15p=3, number_of_45p=3),
            Subject(name="Hóa", grade=Grade.K11, number_of_15p=3, number_of_45p=3),
            Subject(name="Sinh", grade=Grade.K11, number_of_15p=3, number_of_45p=3),
            Subject(name="Văn", grade=Grade.K11, number_of_15p=3, number_of_45p=3),
            Subject(name="Anh", grade=Grade.K11, number_of_15p=3, number_of_45p=3),

            Subject(name="Toán", grade=Grade.K12, number_of_15p=3, number_of_45p=3),
            Subject(name="Lý", grade=Grade.K12, number_of_15p=3, number_of_45p=3),
            Subject(name="Hóa", grade=Grade.K12, number_of_15p=3, number_of_45p=3),
            Subject(name="Sinh", grade=Grade.K12, number_of_15p=3, number_of_45p=3),
            Subject(name="Văn", grade=Grade.K12, number_of_15p=3, number_of_45p=3),
            Subject(name="Anh", grade=Grade.K12, number_of_15p=3, number_of_45p=3),
        ]
        # for subject in subjects:
        #     db.session.add(subject)
        # db.session.commit()

        # create teacher_subject
        teacher_subject =[
            # toán
            TeacherSubject(teacher_id=teacher4.id, subject_id=subjects[0].id),
            TeacherSubject(teacher_id=teacher4.id, subject_id=subjects[6].id),
            TeacherSubject(teacher_id=teacher4.id, subject_id=subjects[12].id),

            # lý
            TeacherSubject(teacher_id=teacher5.id, subject_id=subjects[1].id),
            TeacherSubject(teacher_id=teacher5.id, subject_id=subjects[7].id),
            TeacherSubject(teacher_id=teacher5.id, subject_id=subjects[13].id),

            # hóa
            TeacherSubject(teacher_id=teacher6.id, subject_id=subjects[2].id),
            TeacherSubject(teacher_id=teacher6.id, subject_id=subjects[8].id),
            TeacherSubject(teacher_id=teacher6.id, subject_id=subjects[14].id),

            # sinh
            TeacherSubject(teacher_id=teacher7.id, subject_id=subjects[3].id),
            TeacherSubject(teacher_id=teacher7.id, subject_id=subjects[9].id),
            TeacherSubject(teacher_id=teacher7.id, subject_id=subjects[15].id),

            # van
            TeacherSubject(teacher_id=teacher8.id, subject_id=subjects[4].id),
            TeacherSubject(teacher_id=teacher8.id, subject_id=subjects[10].id),
            TeacherSubject(teacher_id=teacher8.id, subject_id=subjects[16].id),

            # anh
            TeacherSubject(teacher_id=teacher9.id, subject_id=subjects[5].id),
            TeacherSubject(teacher_id=teacher9.id, subject_id=subjects[11].id),
            TeacherSubject(teacher_id=teacher9.id, subject_id=subjects[17].id),
        ]

        # for t_s in teacher_subject:
        #     db.session.add(t_s)
        # db.session.commit()

        semesters = [
            Semester(name=SemesterName.HK1),
            Semester(name=SemesterName.HK2),
        ]
        # for s in semesters:
        #     db.session.add(s)
        # db.session.commit()

        regulations = [
            Regulation(type="Student",regulation_name="Số tuổi của học sinh", min=15, max=18,admin_id=admin.id),
            Regulation(type="Quantity_student",regulation_name="Sỉ số lớp học",min=10,max=40,admin_id=admin.id)
        ]

        # for regulation in regulations:
        #     db.session.add(regulation)
        # db.session.commit()