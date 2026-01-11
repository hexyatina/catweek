from flask import Flask, render_template, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
app = Flask(__name__)


# Database connection - FIXED VERSION
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn


# Home page - show schedule
@app.route('/')
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


# API endpoint for getting schedule by group
@app.route('/api/schedule/<group_name>')
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

    return jsonify(schedule)


if __name__ == '__main__':
    app.run(debug=True)
