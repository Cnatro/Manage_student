import pdb

import pandas
from flask import render_template, url_for, redirect
import random

from wtforms.validators import length

from App import app, login, ALLOW_EXTENSIONS, utils
from App.admin import *
from flask_login import login_user, logout_user, current_user, login_required

from App.model import UserRole, SemesterName, Class, Subject, Semester
from App.decorators import role_only

from App import form
from App.dao.assignment import handle_action
from App.dao import auth, student, teacher_subject, exam, semester, teacher_list, regulation, assignment

from App.api.student_class import *
from App.api.teacher_assignment import *
from App.api.teacher_score import *




# user login
@login.user_loader
def get_user_by_id(user_id):
    return auth.get_user_by_id(user_id)


@app.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.user_role == UserRole.ADMIN:
            return redirect('/admin')
        user_page = current_user.user_role
        return redirect(url_for('home', user_page=user_page))
    return redirect(url_for('login_process'))


@app.route("/login", methods=['GET', 'POST'])
def login_process():
    mse = ""
    form_login = form.loginForm()
    if request.method == "POST" and form_login.validate_on_submit():
        username = form_login.username.data
        password = form_login.password.data
        user_login = auth.auth_user(username=username, password=password)
        if user_login:
            login_user(user_login)
            user_page = user_login.user_role
            return redirect(url_for('index', user_page=user_page))
        mse = "Tên đăng nhập hoặc mật khẩu không chính xác"
    return render_template('login.html', form_login=form_login, mse=mse)


@app.route('/login-admin', methods=['POST'])
def login_admin_process():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user_login = auth.auth_user(username=username, password=password,role=UserRole.ADMIN)
        # pdb.set_trace()
        if user_login:
            login_user(user_login)
    return redirect('/admin')


@app.route("/logout")
def logout_process():
    logout_user()
    return redirect(url_for('login_process'))


@app.route('/home')
@login_required
@role_only([UserRole.TEACHER, UserRole.STAFF])
def home():
    user_page = request.args.get('user_page', default=app.config['USER_STAFF']).split('.')[-1]  # lấy giá trị cuối cùng
    return render_template("index.html",
                           user_page=str.lower(user_page))


# staff
# quản lí học sinh
@app.route('/staff/manage_student', methods=['GET', 'POST'])
@role_only([UserRole.STAFF])
def manage_student():
    form_add_student = form.add_student()
    show_modal = False

    if request.method == "POST":
        if form_add_student.validate_on_submit():
            data = add_student(form_add_student=form_add_student, staff_id=current_user.id)
            student.create_student(**data)
            return redirect(url_for('manage_student'))
        else:
            show_modal = True  # show lại modal khi có lỗi
    students = student_class.load_students()
    class_ = classes.get_list_class()
    return render_template('staff/manage_student.html',
                           form_add_student=form_add_student,
                           students=students,
                           class_=class_,
                           user_page=app.config['USER_STAFF'],
                           show_modal=show_modal)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOW_EXTENSIONS


@app.route('/staff/upload_by_excel', methods=['POST', 'GET'])
@role_only([UserRole.STAFF])
def upload_by_excel():
    if 'upload_file' not in request.files:
        return "Không tồn tại tệp tin", 400
    file = request.files['upload_file']

    if file.filename == '':
        return "File đang trống file dữ liệu"
    if file and allowed_file(file.filename):
        try:
            datat_file = pandas.read_excel(file)
            data = datat_file.to_dict(orient='records')
            # thêm ds hs vào database
            student.add_list_student(list_data=data, staff_id=current_user.id)
            # phân lớp
            quantity_student_allow = regulation.get_regulation_by_name('Quantity_student').max
            quantity_student_less = random.randint(quantity_student_allow - 5, quantity_student_allow)
            student_class.auto_create_class(quantity_student_less)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        return redirect(url_for('manage_student'))
    return "Thêm dữ liệu không thành công"


def add_student(form_add_student, staff_id):
    data = form_add_student.data
    del data['btn_add_student']
    del data['csrf_token']

    data['staff_id'] = staff_id
    data['gender'] = int(data['gender'])
    return data


# quản lí danh sách lớp
@app.route('/staff/classes_View', methods=['GET', 'POST'])
@role_only([UserRole.STAFF])
def class_view():
    if request.method == "POST":
        class_id = request.form.get('class_id')
        student_ids = request.form.getlist('student_id')
        student_class.add_student_class(student_ids=student_ids, class_id=class_id)

    class_ = classes.get_list_class()
    students_no_class = student_class.get_list_student_no_class()
    quantity_student_allow = regulation.get_regulation_by_name('Quantity_student').max
    return render_template('staff/classes_View.html',
                           class_=class_,
                           students_no_class=students_no_class,
                           quantity_student_allow=quantity_student_allow,
                           user_page=app.config['USER_STAFF'])


@app.route('/staff/classes_View/info/<int:class_id>')
@role_only([UserRole.STAFF])
def class_detail(class_id):
    class_ = classes.get_class_by_id(class_id=class_id)
    students = student_class.get_list_student(class_id=class_id)
    return render_template('staff/class_info.html',
                           user_page=app.config['USER_STAFF'],
                           class_=class_,
                           students=students)


# chuyen lớp cho hc sinh
@app.route('/staff/change_class', methods=['GET', 'POST'])
@role_only([UserRole.STAFF])
def change_class():
    if request.method == "POST":
        student_ids = request.form.getlist('student_id')
        class_id = request.form.get('class_id')
        student_class.change_student_to_class(class_id=class_id, student_ids=student_ids)

    quantity_student_allow = regulation.get_regulation_by_name('Quantity_student').max
    classes_none = classes.get_list_class_less_quantity(quantity_student_allow)
    return render_template('/staff/adjust_class.html',
                           classes_none=classes_none,
                           user_page=app.config['USER_STAFF'])


# dieu chinh cho hc sinh len lop
@app.route('/staff/adjust_class', methods=['GET', 'POST'])
@role_only([UserRole.STAFF])
def adjust_class():
    if request.method == "POST":
        grade_id = int(request.form.get('grade_id'))
        if grade_id:
            # lấy thông tin hs cũ và lưu vào file excel
            info_students_old_grade = exam.get_info_old_students(grade_=Grade(grade_id))
            if info_students_old_grade:
                data_old_students = exam.get_info_students_for_excel(old_students=info_students_old_grade)
                utils.export_excel(data=data_old_students, year_learn=data_old_students[0]['learn_year'])
                # cập nhận lại thông tin cho hs lên lớp xóa thông tin cũ
                student_class.update_class(old_students=info_students_old_grade, grade=Grade(grade_id).value)
                student_class.reset_info_students(old_students=info_students_old_grade)
            else:
                return "Thuc hien khong thanh cong"

    return render_template('/staff/adjust_class.html', user_page=app.config['USER_STAFF'])


# phân công giảng dạy
@app.route('/staff/assignment_teacher', methods=['GET', 'POST'])
@role_only([UserRole.STAFF])
def assignment_teach():
    if request.method == 'POST':
        grade = int(request.form.get('grade'))
        class_ = int(request.form.get('class_'))
        return redirect(url_for('teacher_subject_assignment',
                                grade_value=grade,
                                class_id=class_))
    return render_template('staff/assignment_teacher.html', user_page=app.config['USER_STAFF'])


@app.route('/staff/assignment_teacher/<int:grade_value>/<int:class_id>', methods=['GET', 'POST'])
def teacher_subject_assignment(grade_value, class_id):
    semesters = semester.get_semester_by_year(datetime.now().year)
    # xử lí action save and delete
    if request.method == 'POST':
        action_name = request.form.get('action')
        assignment.handle_action(action_name=action_name)(class_id=class_id)
        return redirect(url_for('assignment_teach'))
    # xử lí show khi tìm kiếm grade và class
    plan_class = assignment.load_assignments_of_class(class_id=class_id)
    subjects = teacher_subject.get_subjects_by_grade(Grade(grade_value))
    return render_template('staff/assignment_teacher.html', user_page=app.config['USER_STAFF'],
                           semesters=semesters,
                           plan_class=plan_class,
                           subjects=subjects,
                           grade_value=grade_value,
                           class_id=class_id,
                           class_name=classes.get_class_by_id(class_id).name,
                           get_teachers=teacher_subject.get_all_teacher_by_subject)


# teacher
@app.route('/teacher/teacher_score',methods=['GET','POST'])
@role_only([UserRole.TEACHER])
def teacher_score():
    teach_classes = teacher_list.get_class_by_teacher_id(current_user.id)
    if request.method == "POST":
        class_id = request.form.get('class_id')
        semester_id = request.form.get('semester_id')
        subject_id = request.form.get('subject_id')
        teach_plan = teacher_list.get_plan(class_id=class_id,
                                     semester_id=semester_id,
                                     subject_id=subject_id,
                                     teacher_id=current_user.id)

        return redirect(url_for('view_score',teacher_plan_id=teach_plan.id))

    return render_template('teacher/teacher_score.html',
                           user_page='teacher',
                           teach_classes=teach_classes)


@app.route('/teacher/teacher_input_score/<int:teacher_plan_id>',methods=['GET','POST'])
def input_score(teacher_plan_id):
    teach_plan = teacher_list.get_teaching_plan_by_id(teacher_plan_id=teacher_plan_id)
    return render_template('teacher/teacher_input_score.html',
                           user_page='teacher',
                           teach_plan=teach_plan,
                           get_score=exam.get_score_student)


@app.route('/teacher/view_score/<int:teacher_plan_id>')
def view_score(teacher_plan_id):
    teach_plan = teacher_list.get_teaching_plan_by_id(teacher_plan_id=teacher_plan_id)
    return render_template('teacher/view_score.html',user_page='teacher',
                           teach_plan=teach_plan,
                           get_score=exam.get_score_student)


@app.route('/teacher/view_average_score/<int:teacher_plan_id>')
def view_average_score(teacher_plan_id):
    # Lấy kế hoạch giảng dạy
    teach_plan = teacher_list.get_teaching_plan_by_id(teacher_plan_id=teacher_plan_id)

    # Khởi tạo điểm rỗng cho mỗi học sinh
    student_scores = teacher_list.init_student_scores(teach_plan)

    # Lấy danh sách học kỳ từ năm học
    semesters = teacher_list.get_semesters_by_year(teach_plan.semester.year)

    # Xử lý điểm trung bình cho từng học kỳ
    for semester in semesters:
        teacher_list.process_scores(semester, teach_plan, student_scores)

    # Render template
    return render_template(
        'teacher/view_average_score.html',
        teach_plan=teach_plan,
        user_page='teacher',
        student_scores=student_scores
    )




if __name__ == '__main__':
    app.run(debug=True)