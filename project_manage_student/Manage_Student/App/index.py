import pandas
from flask import render_template, url_for, request, flash, jsonify
from werkzeug.utils import redirect

from App import app, login, ALLOW_EXTENSIONS
from flask_login import login_user, logout_user, current_user,login_required
from App.dao import auth
from App.dao.student import*
from App.model import UserRole
from App.decorators import role_only
from App.form import*


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
        return redirect(url_for('home',user_page=user_page))
    return redirect(url_for('login_process'))


@app.route("/login",methods=['GET','POST'])
def login_process():
    mse =""
    form = loginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_login = auth.auth_user(username=username, password=password)
        if user_login:
            login_user(user_login)
            user_page = user_login.user_role
            return redirect(url_for('home',user_page=user_page))
        mse = "Tên đăng nhập hoặc mật khẩu không chính xác"
    return render_template('login.html',form=form, mse = mse)


@app.route("/logout")
def logout_process():
    logout_user()
    return redirect(url_for('login_process'))


@app.route('/home')
@login_required
@role_only([UserRole.TEACHER,UserRole.STAFF])
def home():
    user_page = request.args.get('user_page',default='staff').split('.')[-1] #lấy giá trị cuối cùng
    return render_template("index.html",user_page=str.lower(user_page))


@app.route('/manage_student')
@role_only([UserRole.STAFF])
def manage_student():
    students = load_students()
    return render_template('manage_student.html',user_page='staff',students=students)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOW_EXTENSIONS


@app.route('/upload_by_excel', methods=['POST','GET'])
@role_only([UserRole.STAFF])
def upload_by_excel():
    if 'upload_file' not in request.files:
        return "Không tồn tại tệp tin",400
    file = request.files['upload_file']

    if file.filename == '':
        return "File đang trống file dữ liệu"
    if file and allowed_file(file.filename):
        try:
            datat_file = pandas.read_excel(file)
            data = datat_file.to_dict(orient='records')
            add_list_student(list_data=data,staff_id=current_user.id)
        except Exception as e:
            return jsonify({'error':str(e)}),500
        return redirect(url_for('manage_student'))

    return "Thêm dữ liệu không thành công"




@app.route('/add_student',methods=['GET','POST'])
@role_only([UserRole.STAFF])
def add_student():
    if request.method == "POST":
        data = request.form.copy()
        del data['btn_add_student']

        data['staff_id'] = current_user.id
        data['gender'] = int(data['gender'])
        create_student(**data)
        return redirect(url_for('manage_student'))
    return 'Thêm dữ liệu không thành công'

if __name__ == '__main__':
    app.run(debug=True)