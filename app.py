from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sql

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'  # Needed for sessions


# Root route to render main_page.html
@app.route('/')
def home():
    return render_template('main_page.html')


@app.route('/users')
def new_student():
    return render_template('signup.html')


@app.route('/addrec', methods=['POST', 'GET'])
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            Name = request.form['na']
            Email = request.form['em']
            Password = request.form['pass']  # No hashing for now

            with sql.connect("we_do.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (Name, Email, Password) VALUES (?, ?, ?)", (Name, Email, Password))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "Error in insert operation"

        finally:
            return render_template("results.html", msg=msg)
            con.close()


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['em']
        password = request.form['pass']

        print(f"Attempting login with email: {email} and password: {password}")  # Debugging

        with sql.connect("we_do.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE Email = ?", (email,))
            user = cur.fetchone()

            print(f"User retrieved: {user}")  # Debugging output to verify user data

            if user and user[3] == password:  # user[3] is the stored password in the database
                session['user_id'] = user[0]  # Store user id in session
                session['user_email'] = user[2]  # Store user email in session (user[2] is email)
                msg = "Login successful!"
                return redirect(url_for('home'))
            else:
                msg = "Invalid email or password"

        print(f"Error message: {msg}")  # Debugging to verify the message being returned
        return render_template("results.html", msg=msg)

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()  # This clears all data in the session (logs the user out)
    return redirect(url_for('home'))  # Redirect to the homepage

@app.route('/list_service')
def list_service():
    return render_template('list_service.html')

@app.route('/home_repairs')
def home_repairs():
    return render_template('category1.html')

@app.route('/service_post')
def service_post():
    return render_template('servicepost1.html')

if __name__ == '__main__':
    app.run(debug=True)
