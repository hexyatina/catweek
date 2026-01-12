from flask import Flask
from flask import request
from markupsafe import escape
from flask import abort, redirect, url_for
from flask import render_template
from studetstvo.data.database import get_Stepanuk_overall_table_data
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', person=name)

@app.route('/lecturers/<lecturer_name>')
def lecturer_table(lecturer_name):
    data = get_lecturer_table_data(lecturer_name)

    return

@app.route('/api/schedule/<group_name>')
def get_schedule(group_name):

@app.route('/Stepanuk')
def Stepanuk_table():
    data = get_Stepanuk_overall_table_data()
    return render_template('index.html', schedule=data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'do_the_login()'
    else:
        return 'show_the_login_form()'

if __name__ == '__main__':
    app.run(debug=True)
