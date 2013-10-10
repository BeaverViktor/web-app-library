from myapp import app
from myapp.users.forms import RegistrationForm, LoginForm
from myapp.users.models import User
from myapp.database import db_session
from myapp.decorators import login_required

from flask import request, flash, redirect, url_for, render_template, session

@app.route('/register/', methods=['GET', 'POST'])
def register():
    errors = []
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        q = User.query
        if q.filter(User.name == form.name.data).first():
            errors.append('Username "{0}" already exists.'
                          .format(form.name.data))
        if q.filter(User.email == form.email.data).first():
            errors.append('Email "{0}" has been already registered.'
                          .format(form.email.data))
        if not errors:
            user = User(form.name.data, form.email.data,
                        form.password.data)
            db_session.add(user)
            db_session.commit()
            flash('Thank you for registration.')
            return redirect(url_for('login'))
    return render_template('users/register.html', form=form, errors=errors)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    errors = []
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.name == form.name.data).first()
        if not user:
            errors.append('"{0}" is invalid username. Please register.'.format(
                form.name.data))
        elif user.password != form.password.data:
            errors.append('Invalid password.')
        else:
            session['user'] = user.name
            flash('You are logged in.')
            return redirect(url_for('index'))
    return render_template('users/login.html', form=form, errors=errors)

@app.route('/logout/')
@login_required
def logout():
    session.pop('user', None)
    flash('You were logged out.')
    return redirect(url_for('index'))