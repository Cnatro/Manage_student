import pandas
from flask import render_template, url_for,redirect
import random

from App import app, login, ALLOW_EXTENSIONS,utils
from flask_login import login_user, logout_user, current_user, login_required

from App.model import UserRole
from App.decorators import role_only

from App.form import *
from App.dao import auth, student, teacher_subject,exam,semester
from App.dao.assignment import handle_action

from App.api.student_class import *
from App.api.teacher_assignment import *




# user login
@login.user_loader
def get_user_by_id(user_id):
    return auth.get_user_by_id(user_id)


@app.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.user_role == UserRole.ADMIN:
            pass
        user_page = current_user.user_role
        return redirect(url_for('home', user_page=user_page))
    return redirect(url_for('login_process'))


@app.route("/login", methods=['GET', 'POST'])
def login_process():
    mse = ""
    form = loginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_login = auth.auth_user(username=username, password=password)
        if user_login:
            login_user(user_login)
            user_page = user_login.user_role
            return redirect(url_for('home', user_page=user_page))
        mse = "Tên đăng nhập hoặc mật khẩu không chính xác"
    return render_template('login.html', form=form, mse=mse)


@app.route("/logout")
def logout_process():
    logout_user()
    return redirect(url_for('login_process'))


@app.route('/home')
@login_required
@role_only([UserRole.TEACHER, UserRole.STAFF])
def home():
    user_page = request.args.get('user_page', default='staff').split('.')[-1]  # lấy giá trị cuối cùng
    return render_template("index.html",
                           user_page=str.lower(user_page))


# staff
# quản lí học sinh
@app.route('/staff/manage_student')
@role_only([UserRole.STAFF])
def manage_student():
    students = student_class.load_students()
    class_ = classes.get_list_class()
    return render_template('staff/manage_student.html',
                           students=students,
                           class_=class_,
                           user_page='staff')


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
            quantity_student_less = random.randint(app.config['QUANTITY_STUDENT'] - 5,app.config['QUANTITY_STUDENT'])
            student_class.auto_create_class(quantity_student_less)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        return redirect(url_for('manage_student'))

    return "Thêm dữ liệu không thành công"


@app.route('/staff/add_student', methods=['GET', 'POST'])
@role_only([UserRole.STAFF])
def add_student():
    if request.method == "POST":
        data = request.form.copy()
        del data['btn_add_student']

        data['staff_id'] = current_user.id
        data['gender'] = int(data['gender'])
        student.create_student(**data)
        return redirect(url_for('manage_student'))
    return 'Thêm dữ liệu không thành công'


# quản lí danh sách lớp
@app.route('/staff/classes_View')
@role_only([UserRole.STAFF])
def create_class():
    class_ = classes.get_list_class()
    class_id = request.form.get('class_id', default=None)
    students_class = student_class.get_list_student_by_class_id(class_id)
    return render_template('staff/classes_View.html',
                           class_=class_,
                           students_class=students_class,
                           user_page='staff')


# chuyen lớp cho hc sinh
@app.route('/staff/change_class',methods=['GET','POST'])
@role_only([UserRole.STAFF])
def change_class():
    classes_none = classes.get_list_class_less_quantity(app.config['QUANTITY_STUDENT'])
    if request.method == "POST":
        student_ids = request.form.getlist('student_id')
        class_id = request.form.get('class_id')
        student_class.change_student_to_class(class_id, student_ids)
    return render_template('/staff/adjust_class.html',
                           classes_none=classes_none,
                           user_page='staff')


# dieu chinh cho hc sinh len lop
@app.route('/staff/adjust_class',methods=['GET','POST'])
@role_only([UserRole.STAFF])
def adjust_class():
    if request.method == "POST":
        grade_id = int(request.form.get('grade_id'))

        # lấy thông tin hs cũ và lưu vào file excel
        info_students_old_grade = exam.get_info_old_students(grade_=Grade(grade_id))
        data_old_students = exam.get_info_students_for_excel(info_students_old_grade)
        utils.export_excel(data=data_old_students,year_learn=data_old_students[0]['learn_year'])

        #cập nhận lại thông tin cho hs lên lớp xóa thông tin cũ
        student_class.update_class(old_students=info_students_old_grade,grade=Grade(grade_id).value)
        student_class.reset_info_students(old_students=info_students_old_grade)

    return render_template('/staff/adjust_class.html', user_page='staff')


# phân công giảng dạy
@app.route('/staff/assignment_teacher', methods=['GET', 'POST'])
@role_only([UserRole.STAFF])
def assignment_teach():
    semesters = semester.get_all_semester()
    # [ print(s.year) for s in semesters ]
    # print(unique_semester(semesters))
    if request.method == 'POST':
        grade = int(request.form.get('grade'))
        class_ = int(request.form.get('class_'))
        return redirect(url_for('teacher_subject_assignment',
                                grade_value=grade,
                                class_id=class_))
    return render_template('staff/assignment_teacher.html', user_page='staff',
                           semesters=semester.unique_semester(semesters))


@app.route('/staff/assignment_teacher/<int:grade_value>/<int:class_id>', methods=['GET', 'POST'])
def teacher_subject_assignment(grade_value, class_id):
    semesters = semester.get_all_semester()
    # xử lí action save and delete
    if request.method == 'POST':
        action_name = request.form.get('action')
        handle_action(action_name)(class_id)

    # xử lí show khi tìm kiếm grade và class
    subjects = teacher_subject.get_subjects_by_grade(Grade(grade_value))
    return render_template('staff/assignment_teacher.html', user_page='staff',
                           semesters=semester.unique_semester(semesters),
                           subjects=subjects,
                           grade_value=grade_value,
                           class_id=class_id,
                           class_name=classes.get_class_by_id(class_id).name,
                           get_teachers=teacher_subject.get_all_teacher_by_subject)


# teacher
@app.route('/teacher_score')
@role_only([UserRole.TEACHER])
def teacher_score():
    return render_template('teacher/teacher_score.html', user_page='staff')



# @app.context_processor
# def common_context_params():
#     return {
#         ''
#     }


if __name__ == '__main__':
    app.run(debug=True)
