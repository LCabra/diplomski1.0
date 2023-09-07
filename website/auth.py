from flask import Blueprint, render_template, request, flash, redirect, url_for
from website import models
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from website import db

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']

        user = models.User.query.filter_by(email=user_email).first()
        if user:
            if check_password_hash(user.password_hash, user_password):
                flash("Logged in successfully!")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, please try again.")
                #return redirect(url_for('login'))
        else:
            flash('Email does not exist.')

    return render_template('login.html', user=current_user)
        # conn = psycopg2.connect(
        #     host='localhost',
        #     user='postgres',
        #     password='zuzuna02',
        #     database='vezbam'
        # )
        # cur = conn.cursor()

        # # Fetch the user's data from the database based on the email
        # cur.execute("SELECT email, password_hash FROM users WHERE email = %s", (user_email,))
        # user_data = cur.fetchone()

        # if user_data and check_password_hash(user_data[1], user_password):
        #     flash(f"Logged in successfully as {user_email}", category='success')
        #     conn.close()
        #     return redirect(url_for('home'))
        # else:
        #     flash("Incorrect email or password. Please try again.", category='error')
        #     conn.close()
        #     return redirect(url_for('login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=["POST","GET"])
def signup():
    if request.method == 'POST':

        user_email = request.form['email']
        user_username = request.form['username']
        user_password = request.form['password']
        user_confirm_password = request.form['confirm_password']

        if len(user_email) < 5:
            flash('Email must be greater than 4 characters.')
        elif len(user_username) < 2:
            flash('Username must be greater than 1 characters.')
        elif user_password != user_confirm_password:
            flash('Passwords don\'t match.')
        else:
            new_user = models.User(email=user_email, username=user_username, password_hash=generate_password_hash(user_password,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!')
            return redirect(url_for('auth.login'))
    
    return render_template('signup.html', user=current_user)