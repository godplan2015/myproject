from flask_sqlalchemy import SQLAlchemy
from myapp import app
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, DataRequired, EqualTo, Email
from wtforms import SelectFieldBase, StringField, DecimalField, SelectField, PasswordField, SubmitField
from werkzeug.security import generate_password_hash, check_password_hash




db = SQLAlchemy(app)


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

# Registration Form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

# Login Form (using Username)
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


with app.app_context():
    db.drop_all()
    db.create_all()