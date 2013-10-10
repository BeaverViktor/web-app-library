from myapp import app
from myapp.database import init_db

init_db()
app.run(debug=True)