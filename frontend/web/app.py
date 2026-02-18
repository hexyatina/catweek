from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', person=name)

#@app.route('/api/schedule/<group_name>')
#   def get_schedule(group_name):

@app.route('/lecturers/<lecturer_name>')
def lecturer_table(lecturer_name):
    data = get_lecturer_table_data(lecturer_name)
    return render_template('index.html', schedule=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'do_the_login()'
    else:
        return 'show_the_login_form()'

if __name__ == '__main__':
    app.run(debug=True)
