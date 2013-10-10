from wtforms import Form, TextField, SelectMultipleField, validators, ValidationError

class AuthorForm(Form):
    name = TextField('Name', [validators.Length(min=4, max=35)])
    
class BookForm(Form):
    name = TextField('Name', [validators.Required(),
                              validators.Length(min=1, max=35)])
    authors = SelectMultipleField('Author(s)', coerce=int)
    
    def validate_authors(form, field):
        if not field.data:
            raise ValidationError('You should choose at least one author.')