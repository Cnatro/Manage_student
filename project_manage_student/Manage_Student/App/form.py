from flask_wtf import FlaskForm
from wtforms.fields import StringField, SelectField, DateField, EmailField, TextAreaField
from wtforms.fields.simple import SubmitField, PasswordField
from wtforms.validators import data_required, Regexp, Length
from datetime import date
from wtforms import ValidationError

def validate_birthday(form,field):
    today = date.today()
    birthday = field.data

    age = today.year - birthday.year - ( (today.month,today.day) < (birthday.month,birthday.day) )

    if age < 15 or age > 20:
        raise ValidationError("Tuổi phải nằm trong khoảng 15 đến 20 tuổi.")




class loginForm(FlaskForm):
    username = StringField("Tên đăng nhập",
                           validators=[data_required(message="Tên đăng nhập không được bỏ trống"),
                                       Length(min=3, max=32,
                                              message="Tên đăng nhập có kích thước phải từ 6 đến 32 kí tự"),
                                       Regexp('(^[A-Za-z0-9_\\.]+$)',
                                              message="Tên đăng nhập gồm các chữ hoa, thường")],
                           render_kw={'class': 'form-control', 'id': 'username', 'placeholder': 'Nhập tên đăng nhâp',
                                      'required': False})

    password = PasswordField("Mật khẩu",
                             validators=[data_required(message="Mật khẩu không được để trống"),
                                         Length(min=5, max=31,
                                                message="Mật khẩu có kích thước phải có kích thước 6 kí tự"),
                                         Regexp('(^([A-Z]){1}([A-Za-z0-9_\\.!@#$%^&*()]+)$)',
                                                message="Mật khẩu phải bắt đầu bằng chữ một chữ cái hoa và một kí tự đặc biệt")],
                             render_kw={'class': 'form-control', 'id': 'password', 'placeholder': "Nhập mật khẩu",
                                        'required': False})
    submit = SubmitField("Đăng nhập")


class add_student(FlaskForm):
    name = StringField("Họ và tên",
                           validators=[data_required(message="Họ và tên không được để trống")],
                           render_kw={"class": "form-control", "id": "fullname", "placeholder": "Nhập họ và tên",
                                      "required": False})

    gender = SelectField("Giới tính",
                         validators=[data_required(message="Không được để trống giới tính")],
                         choices=[('0', 'Nam'), ('1', 'Nữ')],
                         render_kw={"class": "form-select", "id": "gender", "required": False},
                         default='0')

    birthday = DateField('Ngày sinh',
                         validators=[data_required(message="Ngày sinh không được bỏ trống"),
                                     validate_birthday],
                         render_kw={"class": "form-control", 'id': "birthday", "required": False})

    number_phone = StringField("Số điện thoại",
                               validators=[data_required(message="Số điện thoại không được bỏ trống"),
                                           Regexp('(^[0-9]{10}$)',
                                                  message="Số điện thoại phải chứa đúng 10 chữ số và chỉ được nhập số")],
                               render_kw={"class": "form-control", "id": "number_phone", "required": False})

    email = EmailField("Email",
                       validators=[data_required(message="Email không được bỏ trống"),
                                   Regexp('^[A-Za-z0-9_\\.]{2,32}@([a-zA-Z0-9]{2,12})(.[a-zA-Z]{2,12})+$',
                                          message='Email không đúng định dạng (example@gmail.com)')],
                       render_kw={'class': 'form-control', 'id': 'email', "required": False})

    address = TextAreaField("Địa chỉ",
                            validators=[data_required(message="Địa chỉ không được bỏ trống")],
                            render_kw={'class': 'form-control', 'id': "address", "required": False})

    btn_add_student = SubmitField("Ghi nhận", render_kw={'class': 'btn btn-primary'})




