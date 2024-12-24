
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla.fields import QuerySelectField
from sqlalchemy import true
from wtforms import validators
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField
from wtforms import ValidationError

from App import app, db
# from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect, jsonify, request
from App.model import Student, Class, Subject, UserRole, Grade, User, Regulation, TeacherSubject, Profile, Score, \
    Semester
from flask_admin.form import Select2Field
from flask_admin.form.widgets import Select2Widget
from App.dao.stats import get_subjects, get_semesters, get_years, get_grades, get_subjects_by_grade, \
    get_report_data  # Nhập các hàm DAO
from App.api.admin import *




admin = Admin(app=app, name='Admin', template_mode='bootstrap4')

class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class ManageClassView(AdminView):
    def _teacher_name(view, context, model, name):
        return model.user.profile.name  # Lấy tên giáo viên từ quan hệ profile


    column_list = ['id', 'name', 'grade', 'quantity_student', 'teacher_name']
    form_columns = ['name', 'grade', 'quantity_student', 'teacher_id']
    column_formatters = {
        'teacher_name': _teacher_name,  # Định dạng cột teacher_name
    }

    # Thêm các thuộc tính lọc cho các cột
    column_filters = ['name', 'grade', 'quantity_student', 'teacher_id']

    # Thêm các thuộc tính sắp xếp cho các cột
    column_sortable_list = ['name', 'grade', 'quantity_student', 'teacher_id']

    column_labels = {
        'id': 'Mã Lớp',
        'name': 'Tên Lớp',
        'grade': 'Khối',
        'quantity_student': 'Số Lượng Học Sinh',
        'teacher_name': 'Tên Giáo Viên',
    }

    form_extra_fields = {
        'teacher_id': QuerySelectField(
            'Teacher',
            query_factory=User.get_teachers_query,  # Lấy danh sách giáo viên
            get_label=lambda user: user.profile.name,  # Hiển thị tên giáo viên
            widget=Select2Widget(),  # Hiển thị đẹp hơn
            allow_blank=True
        ),
        'quantity_student': IntegerField('Quantity Student', default=0)  # Đặt giá trị mặc định
    }


    def on_model_change(self, form, model, is_created):
        # Kiểm tra nếu teacher_id là đối tượng User
        if isinstance(model.teacher_id, User):
            model.teacher_id = model.teacher_id.id  # Chuyển đổi sang ID
        all_regulations = Regulation.query.all()

        for regulation in all_regulations:
            # Nếu quy định là 15p hoặc 45p, cập nhật các môn học tương ứng
            if "15p" in regulation.type or "45p" in regulation.type:
                subject_name = regulation.type.split('_')[0]  # Lấy tên môn học từ tên quy định
                subjects = Subject.query.filter(Subject.name == subject_name).all()

                for subject in subjects:
                    if "15p" in regulation.type:
                        # Cập nhật số bài kiểm tra 15 phút nếu số bài kiểm tra hiện tại lớn hơn max
                        if subject.number_of_15p > regulation.max:
                            subject.number_of_15p = regulation.max
                    elif "45p" in regulation.type:
                        # Cập nhật số bài kiểm tra 45 phút nếu số bài kiểm tra hiện tại lớn hơn max
                        if subject.number_of_45p > regulation.max:
                            subject.number_of_45p = regulation.max

            # Kiểm tra nếu quy định là Quantity_Class
            if regulation.type == "Quantity_Student":
                # Lấy tất cả các lớp trong bảng Class
                classes = Class.query.all()

                for class_record in classes:
                    # Nếu số lượng học sinh trong lớp > max từ quy định, cập nhật lại số lượng học sinh
                    if class_record.quantity_student > regulation.max:
                        class_record.quantity_student = regulation.max
                        db.session.commit()  # Lưu thay đổi vào cơ sở dữ liệu

        db.session.commit()  # Lưu thay đổi vào cơ sở dữ liệu

        # Gọi phương thức của lớp cha để đảm bảo hành vi mặc định của on_model_change
        super().on_model_change(form, model, is_created)


class ManageSubjectView(AdminView):


    model = Subject  # Áp dụng cho model Subject
    # Hiển thị các cột trong giao diện danh sách
    column_list = ['id', 'name', 'grade', 'number_of_15p', 'number_of_45p']

    # Gán nhãn tiếng Việt cho các cột
    column_labels = {
        'id': 'Mã Môn Học',
        'name': 'Tên Môn Học',
        'grade': 'Khối',
        'number_of_15p': 'Số Lần Kiểm Tra 15 Phút',
        'number_of_45p': 'Số Lần Kiểm Tra 45 Phút'
    }

    # Tìm kiếm theo ID, tên và khối
    column_searchable_list = ['id', 'name', 'grade']

    # Lọc theo các trường
    column_filters = ['id', 'name', 'grade', 'number_of_15p', 'number_of_45p']

    # Cho phép sắp xếp cột
    column_sortable_list = ['id', 'name', 'grade']

    # Thêm thanh tìm kiếm vào giao diện
    form_extra_fields = {
        'grade': Select2Field(
            'Khối',
            choices=[(grade.name, grade.name) for grade in Grade],
            widget=Select2Widget()
        )
    }

    def on_model_change(self, form, model, is_created):
        all_regulations = Regulation.query.all()

        for regulation in all_regulations:
            # Nếu quy định là 15p hoặc 45p, cập nhật các môn học tương ứng
            if "15p" in regulation.type or "45p" in regulation.type:
                subject_name = regulation.type.split('_')[0]  # Lấy tên môn học từ tên quy định
                subjects = Subject.query.filter(Subject.name == subject_name).all()

                for subject in subjects:
                    if "15p" in regulation.type:
                        # Cập nhật số bài kiểm tra 15 phút nếu số bài kiểm tra hiện tại lớn hơn max
                        if subject.number_of_15p > regulation.max:
                            subject.number_of_15p = regulation.max
                    elif "45p" in regulation.type:
                        # Cập nhật số bài kiểm tra 45 phút nếu số bài kiểm tra hiện tại lớn hơn max
                        if subject.number_of_45p > regulation.max:
                            subject.number_of_45p = regulation.max
        super().on_model_change(form, model, is_created)



class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        semesters = get_semesters()  # Danh sách học kỳ
        years = get_years()  # Danh sách năm học
        subjects = db.session.query(Subject).all()

        # Lọc trùng lặp dựa trên tên môn học
        unique_subjects = []
        seen_subject_names = set()
        for subject in subjects:
            if subject.name not in seen_subject_names:
                unique_subjects.append(subject)
                seen_subject_names.add(subject.name)

        return self.render('admin/test.html', subjects=unique_subjects, semesters=semesters, years=years)

    @expose('/report_data')
    def report_data(self):
        grade = request.args.get('grade')
        subject_id = request.args.get('subject')
        semester_id = request.args.get('semester')
        year = request.args.get('year')

        # Get the report data from DAO
        report_data = get_report_data(grade, subject_id, semester_id, year)

        # Return the data as JSON
        return jsonify(report_data)

class RulesView(AdminView):
    column_list = ['id', 'type', 'regulation_name', 'min', 'max']
    form_columns = ['type', 'regulation_name', 'min', 'max']
    column_labels = {
        'id': 'Mã Quy Định',
        'type': 'Loại Quy Định',
        'regulation_name': 'Tên Quy Định',
        'min': 'Giá Trị Tối Thiểu',
        'max': 'Giá Trị Tối Đa',
    }

    def on_model_change(self, form, model, is_created):
        """
        Override phương thức on_model_change để tự động cập nhật bảng Subject và Class khi một quy định thay đổi.
        """
        if is_created:  # Chỉ thực hiện khi tạo mới
            if current_user.user_role.value == 3:  # Kiểm tra quyền admin
                model.admin_id = current_user.id
            else:
                raise ValueError("Chỉ người dùng có quyền 'Admin' mới có thể tạo quy định mới.")

        # Lấy tất cả các quy định trong bảng Regulation
        all_regulations = Regulation.query.all()

        for regulation in all_regulations:
            # Nếu quy định là 15p hoặc 45p, cập nhật các môn học tương ứng
            if "15p" in regulation.type or "45p" in regulation.type:
                subject_name = regulation.type.split('_')[0]  # Lấy tên môn học từ tên quy định
                subjects = Subject.query.filter(Subject.name == subject_name).all()

                for subject in subjects:
                    if "15p" in regulation.type:
                        # Cập nhật số bài kiểm tra 15 phút nếu số bài kiểm tra hiện tại lớn hơn max
                        if subject.number_of_15p > regulation.max:
                            subject.number_of_15p = regulation.max
                    elif "45p" in regulation.type:
                        # Cập nhật số bài kiểm tra 45 phút nếu số bài kiểm tra hiện tại lớn hơn max
                        if subject.number_of_45p > regulation.max:
                            subject.number_of_45p = regulation.max

            # Kiểm tra nếu quy định là Quantity_Class
            if regulation.type == "Quantity_Student":
                # Lấy tất cả các lớp trong bảng Class
                classes = Class.query.all()

                for class_record in classes:
                    # Nếu số lượng học sinh trong lớp > max từ quy định, cập nhật lại số lượng học sinh
                    if class_record.quantity_student > regulation.max:
                        class_record.quantity_student = regulation.max
                        db.session.commit()  # Lưu thay đổi vào cơ sở dữ liệu

        db.session.commit()  # Lưu thay đổi vào cơ sở dữ liệu

        # Gọi phương thức của lớp cha để đảm bảo hành vi mặc định của on_model_change
        super().on_model_change(form, model, is_created)






class ManageTeacherAndStaffView(AdminView):
    model = User
    default_view = 'list'

    # Thêm 'profile.number_phone' và 'profile.address' để hiển thị thông tin từ Profile
    column_list = ['id', 'username', 'user_role', 'profile.name', 'profile.email', 'profile.number_phone',
                   'profile.address']

    column_filters = ['user_role']
    column_sortable_list = ['id', 'username', 'profile.name']

    # Thêm các trường vào form
    form_columns = ['username', 'password', 'user_role', 'profile_name', 'profile_email', 'profile_number',
                    'profile_address']

    form_extra_fields = {
        'profile_name': StringField('Name', validators=[validators.InputRequired()]),
        'profile_email': StringField('Email', validators=[validators.Email(), validators.InputRequired()]),
        # Thêm Email Validator
        'profile_number': StringField('Phone Number', validators=[validators.InputRequired()]),
        # Thêm trường number_phone
        'profile_address': StringField('Address', validators=[validators.Optional()]),  # Thêm trường address
        'user_role': Select2Field(
            'User Role',
            choices=[(role.name, role.name) for role in UserRole if role.name in ['TEACHER', 'STAFF']],
            widget=Select2Widget(),
            validators=[validators.InputRequired()],
            default=UserRole.TEACHER.name,
            coerce=str,
            description="Role của người dùng"
        ),
    }

    def on_model_change(self, form, model, is_created):
        # Nếu đang tạo mới, tự động tạo Profile
        if not model.profile:
            model.profile = Profile()
        model.profile.name = form.profile_name.data
        model.profile.email = form.profile_email.data
        model.profile.number_phone = form.profile_number.data  # Cập nhật number_phone
        model.profile.address = form.profile_address.data  # Cập nhật address
        super().on_model_change(form, model, is_created)


admin.add_view(ManageClassView(Class, db.session, name="Quản Lý Lớp Học"))
admin.add_view(ManageSubjectView(Subject, db.session, name="Quản lý môn học"))
admin.add_view(RulesView(Regulation,db.session,name="Quy định"))
admin.add_view(ManageTeacherAndStaffView(User, db.session, name="Quản lý Nhân sự"))
admin.add_view(StatsView(name="Thống kê điểm"))
admin.add_view(LogoutView(name='Đăng Xuất'))
