from flask import render_template, url_for, request
from werkzeug.utils import redirect

from App import app, login
from flask_login import login_user, logout_user, current_user,login_required
from App.dao import auth
from App.model import UserRole


# user login
@login.user_loader
def get_user_by_id(user_id):
    return auth.get_user_by_id(user_id)


@app.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.user_role == UserRole.ADMIN:
            pass
        return redirect(url_for('home'))
    return redirect(url_for('login_process'))


@app.route("/login",methods=['GET','POST'])
def login_process():
    if request.method == "POST" :
        username = request.form.get('username')
        password = request.form.get('password')

        user_login = auth.auth_user(username=username, password=password)
        if user_login:
            login_user(user_login)

            return redirect(url_for('home'))
    return render_template('login.html')


@app.route("/logout")
def logout_process():
    logout_user()
    return redirect(url_for('login_process'))


@app.route('/home')
@login_required
# @role_only([UserRole.STAFF, UserRole.TEACHER])
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)