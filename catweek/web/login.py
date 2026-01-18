from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @staticmethod
    def get(user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT userid, username FROM users WHERE userid = %s', (user_id,))
        user_data = cur.fetchone()
        cur.close()
        conn.close()

        if user_data:
            return User(user_data['userid'], user_data['username'])
        return None

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT userid, username, password FROM users WHERE username = %s', (username,))
        user_data = cur.fetchone()
        cur.close()
        conn.close()
        return user_data


# Database connection - FIXED VERSION
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Home page - show schedule
@app.route('/')
@login_required
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    # Get all schedule data with joins
    cur.execute('''SELECT t.timestart,
                       t.timeend,
                       g.groupname,
                       l.lessonname,
                       d.dayname,
                       lec.lecturername,
                       p.cabinet,
                       p.url
                FROM overall o
                         JOIN times t ON o.lessontime = t.timeid
                         JOIN ipz_groups g ON o.groupnames = g.groupid
                         JOIN lessons l ON o.lesson = l.lessonid
                         JOIN days d ON o.dayname = d.dayid
                         JOIN lecturers lec ON o.lecturer = lec.lecturerid
                         JOIN places p ON o.place = p.placeid
                ORDER BY d.dayid, t.timeid''')

    schedule = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index.html', schedule=schedule)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        errors = []
        """if len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters long.')
        if password != confirm_password:
            errors.append('Passwords do not match.')"""
        #ill return it on final release

        if not errors:
            conn = get_db_connection()
            cur = conn.cursor()

            # Check if username exists
            cur.execute('SELECT userid FROM users WHERE username = %s', (username,))
            if cur.fetchone():
                errors.append('Username already exists. Please choose a different one.')
            else:
                # Create new user
                hashed_password = generate_password_hash(password)
                try:
                    cur.execute(
                        'INSERT INTO users (username, password) VALUES (%s, %s)',
                        (username, hashed_password)
                    )
                    conn.commit()
                    flash('Account created successfully! You can now log in.', 'success')
                    cur.close()
                    conn.close()
                    return redirect(url_for('login'))
                except Exception as e:
                    conn.rollback()
                    errors.append('An error occurred. Please try again.')

            cur.close()
            conn.close()

        for error in errors:
            flash(error, 'error')

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user_data = User.get_by_username(username)

        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data['userid'], user_data['username'])
            login_user(user)
            flash(f"Welcome back, {user.username}!", 'success')

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
"""@app.route('/<group_name>')
def get_schedule(group_name):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''SELECT t.timestart,
                       t.timeend,
                       g.groupname,
                       l.lessonname,
                       d.dayname,
                       lec.lecturername,
                       p.cabinet,
                       p.url
                FROM overall o
                         JOIN times t ON o.lessontime = t.timeid
                         JOIN ipz_groups g ON o.groupnames = g.groupid
                         JOIN lessons l ON o.lesson = l.lessonid
                         JOIN days d ON o.dayname = d.dayid
                         JOIN lecturers lec ON o.lecturer = lec.lecturerid
                         JOIN places p ON o.place = p.placeid
                WHERE g.groupname = %s
                ORDER BY d.dayid, t.timeid''', (group_name,))

    schedule = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(schedule)"""


if __name__ == '__main__':
    app.run(debug=True)
