from website import models
from flask import render_template, request, Blueprint, redirect, url_for, flash
import psycopg2
from flask_login import login_required, current_user
from website import  db
import datetime
from sqlalchemy import func

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
    

# views.py

# ... (other imports and routes)

@views.route('/pitch/<pitch_name>')
def pitch(pitch_name):
    # Query the database to get pitch data based on pitch name
    pitch_data = get_pitch_by_name(pitch_name)  # Replace with your data retrieval logic
    todays_date = datetime.date.today().strftime("%d-%m-%Y")
    
    conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='zuzuna02',
            database='vezbam'
        )
    
    cur = conn.cursor()
    cur.execute("SELECT pitch_id, match_id, time, date, max_players, availability, COALESCE(array_length(current_players, 1), 0) as current_players "
            "FROM matches "
            "WHERE date::date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '6 days'")
    table = cur.fetchall()

    conn.close()

    if pitch_data:
        pitch_id = pitch_data['pitch_id']

        # Retrieve the corresponding match using pitch_id and date
        match = models.Match.query.filter_by(pitch_id=pitch_id, date=todays_date).first()

        return render_template('pitch.html', user=current_user, pitch_data=pitch_data, pitch_id=pitch_id, todays_date=todays_date, table=table, match=match)
    else:
        # Handle the case where the pitch with the given name is not found
        return render_template('pitch_not_found.html')



@views.route('/join-match/<int:match_id>', methods=['POST'])
@login_required
def join_match(match_id):
    conn = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='zuzuna02',
        database='vezbam'
    )
    cur = conn.cursor()
    cur.execute('SELECT pitches.name '
                'FROM matches '
                'JOIN pitches ON matches.pitch_id=pitches.pitch_id '
                'WHERE current_players IS NOT NULL ' 
                'AND (SELECT array_length(current_players, 1)) <= max_players '
                'AND match_id = %s',(match_id, ))
    pitch_name = cur.fetchone()

    cur.execute('SELECT current_players '
                'FROM matches '
                'WHERE current_players IS NOT NULL ' 
                'AND (SELECT array_length(current_players, 1)) <= max_players '
                'AND match_id = %s',(match_id, ))
    playing = cur.fetchall() # igraci koji igraju X termin

    player = { 'username': current_user.username} # ovo je username od trenutno logovanog usera
    #vraca true ili false ako se player nalazi u playing, u prevodu ako trenutno logovani userov username se nalazi u listi igraca koji igraju X termin
    user_found = any(player['username'] in user_tuple[0] for user_tuple in playing)
    
    #proveravamo da li je igrac vec u matchu, ako jeste vraca poruku da vec igra
    #ako nije onda ga joinuje u match
    if user_found:
        flash(f"Already playing {match_id} match.")
        return redirect(url_for('views.pitch', pitch_name = pitch_name[0]))
    else:
        cur.execute('UPDATE matches SET current_players = array_append(current_players, %s) WHERE match_id = %s',
                (current_user.username, match_id))
        flash(f"{current_user.username.capitalize()} has joined the match {match_id}.")
        conn.commit()
    
    conn.close()

    return redirect(url_for('views.home'))


# Create a route to display the user's matches
@views.route('/your-matches', methods=['POST','GET'])
@login_required
def your_matches():
    if request.method == 'POST':
        pass

    conn = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='zuzuna02',
        database='vezbam'
    )

    cur = conn.cursor()
    cur.execute("SELECT matches.match_id, pitches.pitch_id, pitches.name, matches.time, matches.date, matches.current_players, pitches.image, pitches.address FROM matches JOIN pitches ON matches.pitch_id=pitches.pitch_id WHERE %s IN (SELECT UNNEST(current_players)) ORDER BY matches.time ",(current_user.username,))
    table = cur.fetchall()
    conn.close()

    return render_template('your_matches.html', user=current_user, table=table)


@views.route('/leave-match/<int:match_id>', methods=['POST'])
@login_required
def leave_match(match_id):
    # Fetch the match from the database
    match = models.Match.query.get(match_id)

    if match:
        # Check if the user is in the match's current players list
        if current_user.username in match.current_players:
            try:
                # Create a PostgreSQL connection
                conn = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='zuzuna02',
                    database='vezbam'
                )
                cur = conn.cursor()

                # Execute SQL to remove the user from the current_players array
                cur.execute("""
                    UPDATE matches
                    SET current_players = array_remove(current_players, %s)
                    WHERE match_id = %s;
                """, (current_user.username, match_id))

                # Commit the transaction
                conn.commit()

                flash('You have left the match successfully!', 'success')
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'error')
            finally:
                # Close the cursor and the database connection
                cur.close()
                conn.close()
        else:
            flash('You are not in this match.', 'warning')
    else:
        flash('Match not found.', 'error')

    # Redirect the user back to their matches page
    return redirect(url_for('views.your_matches'))