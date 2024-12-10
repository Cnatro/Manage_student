from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def role_only(roles):
    def wrap(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.user_role not in roles:
                flash("Quyền truy cập không phù hợp")
                return redirect(url_for('login_process'))
            else:
                return f(*args, **kwargs)
        return decorated_function
    return wrap
