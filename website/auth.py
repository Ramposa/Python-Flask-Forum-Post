from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST': # Basic check
        email = request.form.get("email") # Define from form
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first() # This will check if user exist in the database.
        if user: # If the user exist,
            if check_password_hash(user.password, password): # Check if the hash is the same to the existing user. HOWEVER it will pass the hash first then the plain text.
                flash("Logged in success!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else: # If incorrect then it will pass an catagory error.
                flash('Password is incorrect. Please try again', category='error')
        else:
            flash('Email does not exist in the database.', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password") # pwd
        confirmPassword = request.form.get("confirmPassword") # conPwd will check pwd

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email address Already Exist.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password != confirmPassword: # check if pwd IS NOT EQUAL to conPwd which its not the same spits error.
            flash('Password did not match!', category='error')
            
        elif len(username) < 2: #  if user name char length is less than 2 spits error
            flash('Username is too short. Please type in more than 2 charcters', category='error')
        elif len(password) < 6: # if char for password length is less than 6 spits error
            flash('Password is too short. Please type in more than 6 character.', category='error')
        elif len(email) < 4: # if email char is less than 4, spits error
            flash("Invalid email address. Due to email character length is less than 4.", category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash( # NOTE: This stores the password hashed which is encrypted with SHA256
                password, method='SHA256')) # Encryption method = sha256
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required # This function is only accessible if your already logged in.
def logout(): # This function exist only if the user is able to login and want to log out.
    logout_user()
    return redirect(url_for("views.home"))
