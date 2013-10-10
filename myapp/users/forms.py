from wtforms import Form, TextField, PasswordField, validators

class RegistrationForm(Form):
    name = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Email()])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.Length(min=3, max=35),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    name = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.Required(),
        validators.Length(min=3, max=35)
    ])