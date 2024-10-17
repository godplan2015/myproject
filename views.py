from flask import Blueprint, jsonify, request,render_template,flash,session,redirect,url_for
from myapp import app
from model import db
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from model import myform
from model import Register_form
api_blueprint = Blueprint('api_blueprint', __name__)
app.secret_key = 'your_secret_key' 


@api_blueprint.route('/')
@api_blueprint.route('/home')
def home():
    return render_template("homes.html")

@api_blueprint.route('/about')
def about():
    return render_template("about.html")


@api_blueprint.route('/login', methods=['GET','POST'])
def login():
    form = myform()
    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password = request.form.get("password")
        flash("Login successful!")
        return redirect('home')
    
    return render_template('logins.html') 
      

@api_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = myform()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            passwor = form.passwor.data
            confirm= form.confirm.data
            existing_username = user.query.filter_by(username=username).first()
            if existing_username:
                flash('This user has been already taken. Try another one.', 'warning')
                return render_template('logins.html', form=form)
            user = user(username, passwor, confirm)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful!")
    return render_template('registers.html',form=form) 


app.register_blueprint(api_blueprint)


if __name__ == '__main__':
    app.run(debug=True)