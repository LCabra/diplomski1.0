from flask import Flask, request, render_template, redirect, url_for, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import psycopg2   
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DB_NAME = 'vezbam.db'

app = Flask(__name__)

app.secret_key = "beb9f203b24e3db2a29ca4a434073928433e5ab3bdbefdd9a26199c741799ed1"
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:zuzuna02@localhost/{DB_NAME}'
db.init_app(app)

# def create_database(app):
#     if not os.path.exists('website/' + DB_NAME):
#         with app.app_context():
#             db.create_all()
#         print('Created Database!')

# Call the create_database function before running the app
# create_database(app)

@app.route('/', methods=['POST','GET'])
def home():
    conn = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='zuzuna02',
        database='vezbam'
    )
    cur = conn.cursor()
    cur.execute('SELECT * FROM pitches')
    pitch_list = cur.fetchall()
    
    return render_template('home.html', pitch_list=pitch_list)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']

        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='zuzuna02',
            database='vezbam'
        )
        cur = conn.cursor()

        # Fetch the user's data from the database based on the email
        cur.execute("SELECT email, password_hash FROM users WHERE email = %s", (user_email,))
        user_data = cur.fetchone()

        if user_data and check_password_hash(user_data[1], user_password):
            flash(f"Logged in successfully as {user_email}", category='success')
            conn.close()
            return redirect(url_for('home'))
        else:
            flash("Incorrect email or password. Please try again.", category='error')
            conn.close()
            return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/signup', methods=["POST","GET"])
def signup():
    if request.method == 'POST':

        user_email = request.form['email']
        user_username = request.form['username']
        user_password = request.form['password']
        user_confirm_password = request.form['confirm_password']

        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='zuzuna02',
            database='vezbam'
        )
        cur = conn.cursor()

        cur.execute("SELECT email FROM users")
        rows = cur.fetchall()
        password = generate_password_hash(user_password, method='sha256')
        for row in rows:
            if user_email == row[0]:
                flash("Email is already taken. Please choose another email.", category='error')
                return redirect(url_for('signup'))
            
        # If no duplicate email found, proceed to insert
        cur.execute("INSERT INTO users (email, username, password_hash)"
                    "VALUES (%s, %s, %s)",(user_email, user_username, password))
        conn.commit()
        flash("Account created successfully! You can now log in.",category='success')

        cur.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('signup.html')

# TERENI

def get_pitch_by_name(pitch):
    conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='zuzuna02',
            database='vezbam'
        )
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM pitches WHERE name ILIKE %s", (pitch,))
    # Fetch the first matching row
    row = cur.fetchone()
    conn.close()

    if row:
        # Get column names from cur.description
        column_names = [desc[0] for desc in cur.description]
        # Create a dictionary using column names as keys and row values as values
        pitch_data = dict(zip(column_names, row))
        return(pitch_data)
    else:
        return(None)
    

@app.route('/pitch/<pitch_name>')
def pitch(pitch_name):
    # Query the database to get pitch data based on pitch name
    pitch_data = get_pitch_by_name(pitch_name)  # Replace with your data retrieval logic
    
    if pitch_data:
        pitch_id = pitch_data['pitch_id']
        return render_template('pitch.html', pitch_data=pitch_data, pitch_id=pitch_id)
    else:
        # Handle the case where the pitch with the given name is not found
        return render_template('pitch_not_found.html')


@app.route('/classics')
def classics():
    return render_template('classics.html')


if __name__ == '__main__':
    app.run(debug=True)