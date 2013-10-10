from myapp.database import db_session
from myapp.search.forms import SearchForm

from flask import Flask, g

SECRET_KEY = 'you_will_never_know'

app = Flask(__name__)
app.config.from_object(__name__)

import myapp.library.views
import myapp.users.views
import myapp.search.views

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    
@app.before_request
def before_request():
    g.search_form = SearchForm()