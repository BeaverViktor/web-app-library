from wtforms import Form, TextField, validators, SelectField

class SearchForm(Form):
    canon = SelectField('What', choices=[
        ('library', 'Library'), ('books', 'Books'), ('authors', 'Authors')
    ])
    query = TextField('Search', [validators.Required()])