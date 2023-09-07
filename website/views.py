from website import models
from flask import render_template, request, Blueprint
import psycopg2
from flask_login import login_required, current_user
from website import  db

views = Blueprint('views',__name__)

@views.route('/', methods=['POST','GET'])
@login_required
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
    
    return render_template('home.html', user=current_user, pitch_list=pitch_list)

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)

@views.route('/support')
def support():
    return render_template('support.html', user=current_user)


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
    

@views.route('/pitch/<pitch_name>')
def pitch(pitch_name):
    # Query the database to get pitch data based on pitch name
    pitch_data = get_pitch_by_name(pitch_name)  # Replace with your data retrieval logic
    
    if pitch_data:
        pitch_id = pitch_data['pitch_id']
        return render_template('pitch.html', user=current_user, pitch_data=pitch_data, pitch_id=pitch_id)
    else:
        # Handle the case where the pitch with the given name is not found
        return render_template('pitch_not_found.html')


@views.route('/classics')
def classics():
    return render_template('classics.html')