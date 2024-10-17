from flask_sqlalchemy import SQLAlchemy
from myapp import app
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired,DataRequired
from wtforms import SelectFieldBase, StringField, DecimalField, SelectField, PasswordField



db = SQLAlchemy(app)

class Register_form(FlaskForm):
    username =StringField('username', [InputRequired()])
    passwor =PasswordField('passwor', [InputRequired()])
    confirm=PasswordField('confirm', [InputRequired()])

class myform():
    username = db.Column(db.String(55), primary_key=True)
    passwor = db.Column(db.Integer,nullable=False)
    confirm = db.Column(db.Integer,nullable=True)
    

with app.app_context():
    db.drop_all()
    db.create_all()
