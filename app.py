from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import login_user, login_required, logout_user, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

# Configure the SQLite database URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_plug.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Add your secret key here
# Initialize the database
db = SQLAlchemy(app)


# Define a User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Add this line

    def __repr__(self):
        return f"<User {self.username}>"


# Define a SmartPlugUsage model to track plug usage
class SmartPlugUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Float, nullable=False)  # Duration of plug use in minutes

    # Establish a relationship between User and PlugUsage
    user = db.relationship('User', backref=db.backref('usage_logs', lazy=True))

    def __repr__(self):
        return f"<SmartPlugUsage {self.id} by {self.user_id}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Here you would create a new user in the database
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))  # Redirect to login page
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the user from the database
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)  # Log the user in
            return redirect(url_for('dashboard'))  # Redirect to the dashboard
        else:
            flash('Invalid username or password')  # Show error message

    return render_template('login.html')  # Render the login page


# Flask-Login requirements
@property
def is_active(self):
    return True  # Change this logic if you need to deactivate users


@property
def is_authenticated(self):
    return True  # Always true if a user is authenticated


@property
def is_anonymous(self):
    return False  # This is set to false because the user is authenticated


@login_manager.user_loader
def get_user(ident):
    return User.query.get(int(ident))

def get_id(self):
    return str(self.id)  # Flask-Login requires this method to return a unique identifier


@app.route('/success')
def success():
    return "Registration successful!"


@app.route('/')
def home():
    return jsonify(message="Welcome to the Smart Plug Web App")


@app.route('/about')
def about():
    return "This app allows you to control smart plugs."


@app.route('/dashboard')
def dashboard():
    return "This app allows you to control smart plugs."


@app.route('/users')
def list_users():
    users = User.query.all()
    user_list = [{"username": user.username, "email": user.email} for user in users]
    return jsonify(user_list)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
