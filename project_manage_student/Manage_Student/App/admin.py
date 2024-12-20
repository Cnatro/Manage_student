from flask_admin import Admin, BaseView,expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user,logout_user
from App.model import *
from App import app,db
from flask import redirect
from flask_admin.form import Select2Field


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin = Admin(app=app,name='ECommerce Admin',template_mode='bootstrap4')
admin.add_view(AdminView(Class,db.session))
admin.add_view(AdminView(Subject,db.session))
admin.add_view(LogoutView(name='Dang Xuat'))