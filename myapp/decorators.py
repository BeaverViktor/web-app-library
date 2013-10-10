from functools import wraps
from flask import request, session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user', None):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function