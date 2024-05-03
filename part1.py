from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'username'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database_name'

mysql = MySQL(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    if user and user[2] == password: # Assuming password is at index 2
        # Login successful
        session['user_id'] = user[0] # Assuming user_id is at index 0
        return redirect(url_for('modules'))
    else:
        # Login failed
        return render_template('login.html', error='Wrong username or password')

@app.route('/modules')
def modules():
    if 'user_id' in session:
        # User is logged in, you can implement your module logic here
        return "Welcome to Modules page"
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
