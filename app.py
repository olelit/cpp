from flask import Flask
from flask_breadcrumbs import Breadcrumbs
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = '3MPH8oY2EAgbLVy7RBMinwcBntggi7qeG3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Breadcrumbs(app=app)


from views import *

if __name__ == '__main__':
    db.init_app(app)
    csrf.init_app(app)
    app.run()
