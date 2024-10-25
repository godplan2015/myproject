from flask import Blueprint, jsonify, request, render_template, flash, session, redirect, url_for
from myapp import app
from model import db, User
from flask_wtf import FlaskForm
from model import RegisterForm, LoginForm, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required, LoginManager

api_blueprint = Blueprint('api_blueprint', __name__)
app.secret_key = 'your_secret_key'  # Ideally, use environment variables for this.

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)  # Link LoginManager with your app
login_manager.login_view = 'api_blueprint.login' 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@api_blueprint.route('/')
@api_blueprint.route('/home')
def home():
    return render_template("homes.html")


@api_blueprint.route('/about')
def about():
    return render_template("about.html")


@api_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Redirect if already logged in
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)  # Optionally, use login_user(user, remember=True) for "remember me"
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to home or dashboard
        else:
            flash('Login failed. Check your email or password.', 'danger')

    return render_template('logins.html', form=form)

@api_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('This username is already taken. Try another one.', 'warning')
            return render_template('registers.html', form=form)
        
        # Hash the password for security before saving it to the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!", 'success')
        return redirect(url_for('api_blueprint.login'))

    return render_template('registers.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", 'success')
    return redirect(url_for('api_blueprint.login'))


app.register_blueprint(api_blueprint)


if __name__ == '__main__':
    app.run(debug=True)
