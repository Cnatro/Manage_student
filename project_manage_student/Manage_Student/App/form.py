from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import data_required, Regexp, Length


class loginForm(FlaskForm):
    username = StringField(validators=[data_required(message="Tên đăng nhập không được bỏ trống"),
                                       Length(min=6, max=32,
                                              message="Tên đăng nhập có kích thước phải từ 6 đến 32 kí tự"),
                                       Regexp('(^[A-Za-z0-9_\\.]+$)',
                                              message="Tên đăng nhập gồm các chữ hoa, thường")])
    password = StringField(validators=[data_required(message="Mật khẩu không được để trống"),
                                       Length(min=5, max=31,
                                              message="Mật khẩu có kích thước phải có kích thước 6 kí tự"),
                                       Regexp('(^([A-Z]){1}([A-Za-z0-9_\\.!@#$%^&*()]+)$)',
                                              message="Mật khẩu phải bắt đầu bằng chữ một chữ cái hoa và một kí tự đặc biệt")])
    submit = SubmitField("Đăng nhập")
