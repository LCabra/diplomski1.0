# "from flask import Flask, request, render_template, redirect, url_for, flash, g
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import login_user, login_required, logout_user, current_user
# import psycopg2   
# from flask_sqlalchemy import SQLAlchemy
# import os
# from fajlovi import models

# DB_NAME = 'vezbam.db'
# db = SQLAlchemy()

# app = Flask(__name__)
# app.secret_key = "beb9f203b24e3db2a29ca4a434073928433e5ab3bdbefdd9a26199c741799ed1"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:zuzuna02@localhost:5432/vezbam'

# db.init_app(app)


# @app.route('/', methods=['POST','GET'])
# def home():
#     conn = psycopg2.connect(
#         host='localhost',
#         user='postgres',
#         password='zuzuna02',
#         database='vezbam'
#     )
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM pitches')
#     pitch_list = cur.fetchall()
    
#     return render_template('home.html', pitch_list=pitch_list)

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/support')
# def support():
#     return render_template('support.html')

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         user_email = request.form['email']
#         user_password = request.form['password']

#         user = models.User.query.filter_by(email=user_email).first()
#         if user:
#             if check_password_hash(user.password_hash, user_password):
#                 flash("Logged in successfully!")
#                 return redirect(url_for('home'))
#             else:
#                 flash("Incorrect password, please try again.")
#                 #return redirect(url_for('login'))
#         else:
#             flash('Email does not exist.')

#     return render_template('login.html')
#         # conn = psycopg2.connect(
#         #     host='localhost',
#         #     user='postgres',
#         #     password='zuzuna02',
#         #     database='vezbam'
#         # )
#         # cur = conn.cursor()

#         # # Fetch the user's data from the database based on the email
#         # cur.execute("SELECT email, password_hash FROM users WHERE email = %s", (user_email,))
#         # user_data = cur.fetchone()

#         # if user_data and check_password_hash(user_data[1], user_password):
#         #     flash(f"Logged in successfully as {user_email}", category='success')
#         #     conn.close()
#         #     return redirect(url_for('home'))
#         # else:
#         #     flash("Incorrect email or password. Please try again.", category='error')
#         #     conn.close()
#         #     return redirect(url_for('login'))

#     return render_template('login.html')



# @app.route('/signup', methods=["POST","GET"])
# def signup():
#     if request.method == 'POST':

#         user_email = request.form['email']
#         user_username = request.form['username']
#         user_password = request.form['password']
#         user_confirm_password = request.form['confirm_password']

#         if len(user_email) < 5:
#             flash('Email must be greater than 4 characters.')
#         elif len(user_username) < 2:
#             flash('Username must be greater than 1 characters.')
#         elif user_password != user_confirm_password:
#             flash('Passwords don\'t match.')
#         else:
#             new_user = models.User(email=user_email, username=user_username, password_hash=generate_password_hash(user_password,method='sha256'))
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Account created!')
#             return redirect(url_for('login'))
    
#     return render_template('signup.html')

# # TERENI

# def get_pitch_by_name(pitch):
#     conn = psycopg2.connect(
#             host='localhost',
#             user='postgres',
#             password='zuzuna02',
#             database='vezbam'
#         )
    
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM pitches WHERE name ILIKE %s", (pitch,))
#     # Fetch the first matching row
#     row = cur.fetchone()
#     conn.close()

#     if row:
#         # Get column names from cur.description
#         column_names = [desc[0] for desc in cur.description]
#         # Create a dictionary using column names as keys and row values as values
#         pitch_data = dict(zip(column_names, row))
#         return(pitch_data)
#     else:
#         return(None)
    

# @app.route('/pitch/<pitch_name>')
# def pitch(pitch_name):
#     # Query the database to get pitch data based on pitch name
#     pitch_data = get_pitch_by_name(pitch_name)  # Replace with your data retrieval logic
    
#     if pitch_data:
#         pitch_id = pitch_data['pitch_id']
#         return render_template('pitch.html', pitch_data=pitch_data, pitch_id=pitch_id)
#     else:
#         # Handle the case where the pitch with the given name is not found
#         return render_template('pitch_not_found.html')


# @app.route('/classics')
# def classics():
#     return render_template('classics.html')


# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)