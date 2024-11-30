from flask import render_template, url_for, request
from werkzeug.utils import redirect

from App import app, login
from flask_login import login_user, logout_user, current_user,login_required
from App.dao import auth
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


if __name__ == '__main__':
    app.run(debug=True)