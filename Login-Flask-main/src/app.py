import sqlite3
import contextlib
import re
import random

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask import (
    Flask, render_template, 
    request, session, redirect, flash
)

from create_database import setup_database, insert_user
from utils import login_required, set_session

#otp
import random
import smtplib
from email.message import EmailMessage


app = Flask(__name__)
app.secret_key = 'xpSm7p5bgJY8rNoBjGWiz5yjxM-NEBlW6SIBI62OkLc='

database = "users.db"
setup_database(name=database)


@app.route('/otp', methods=['GET', 'POST'])
def otp_verification():
    if request.method == 'GET':
        return render_template('otp.html')

    # Get the OTP entered by the user
    otp = request.form.get('otp')

    # Retrieve the OTP from the session
    expected_otp = session.get('otp_code')

    # Verify the OTP
    if otp != expected_otp:
        flash('Incorrect OTP, please try again', 'error')
        return redirect('/otp')

    # OTP verified, clear from session
    session.pop('otp_code', None)
    flash('OTP verified successfully', 'success')
    return redirect('/')

@app.route('/resend_otp')
def resend_otp():
    email = session.get('email')  # Retrieve the email from the session
    if not email:
        flash("Session expired. Please log in again.", "error")
        return redirect('/login')

    otp_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
    session['otp_code'] = otp_code  # Store the new OTP in the session

    # Send the new OTP via email
    otp(email)
    
    flash("A new OTP has been sent to your email.", "success")
    return redirect('/otp')



@app.route('/')
@login_required
def index():
    print(f'User data: {session}')
    return render_template('index.html', username=session.get('username'))


@app.route('/logout')
def logout():
    session.clear()
    session.permanent = False
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # Set data to variables
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Attempt to query associated user data
    query = 'select username, password, email from users where email = :email'

    with contextlib.closing(sqlite3.connect(database)) as conn:
        with conn:
            account = conn.execute(query, {'email': email}).fetchone()

    if not account: 
        return render_template('login.html', error='Email does not exist')

    # Verify password
    try:
        ph = PasswordHasher()
        ph.verify(account[1], password)
    except VerifyMismatchError:
        return render_template('login.html', error='Incorrect password')

    # Check if password hash needs to be updated
    if ph.check_needs_rehash(account[1]):
        query = 'update users set password = :password where email = :email'
        params = {'password': ph.hash(password), 'username': account[2]}

        with contextlib.closing(sqlite3.connect(database)) as conn:
            with conn:
                conn.execute(query, params)

    # Set cookie for user session
    set_session(
        username=account[0], 
        email=account[2], 
        remember_me='remember-me' in request.form
    )
    
    otp(account[2])
    
    return redirect('/otp')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
     
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    username = request.form.get('username')
    email = request.form.get('email')

    query = 'select username from users where username = :username;'
    with contextlib.closing(sqlite3.connect(database)) as conn:
        with conn:
            result = conn.execute(query, {'username': username}).fetchone()

    if result:
        return render_template('register.html', error='Username already exists')

   
    if len(password) < 8:
        return render_template('register.html', error='Your password must be 8 or more characters')
    if not re.search(r'[A-Z]', password):
        return render_template('register.html', error='Your password must contain at least one uppercase letter')
    if not re.search(r'[a-z]', password):
        return render_template('register.html', error='Your password must contain at least one lowercase letter')
    if not re.search(r'\d', password):
        return render_template('register.html', error='Your password must contain at least one number')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return render_template('register.html', error='Your password must contain at least one special character')
    if password != confirm_password:
        return render_template('register.html', error='Passwords do not match')
    if not re.match(r'^[a-zA-Z0-9]+$', username):
        return render_template('register.html', error='Username must only be letters and numbers')
    if not 3 < len(username) < 26:
        return render_template('register.html', error='Username must be between 4 and 25 characters')

    pw = PasswordHasher()
    hashed_password = pw.hash(password)

    query = 'insert into users(username, password, email) values (:username, :password, :email);'
    params = {
        'username': username,
        'password': hashed_password,
        'email': email
    }

    try:
        with contextlib.closing(sqlite3.connect(database)) as conn:
            with conn:
                conn.execute(query, params)
    except Exception as e:
        return render_template('register.html', error=f'Error registering user: {str(e)}')

    # Generate OTP and set in session
    otp_code = str(random.randint(100000, 999999))
    session['otp_code'] = otp_code

    # Send OTP via email
    otp(email)

    # Set session for the user and redirect to OTP verification
    set_session(username=username, email=email)
    return redirect('/otp')




def otp(email):
    otp_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
    
    session['otp_code'] = otp_code
    print(otp_code)  # Debug: Ensure the OTP is generated

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable encryption

        from_email = 'dennisswanhtet@gmail.com'
        password = 'nbwo vuit ywbl shrf'

        server.login(from_email, password)

        msg = EmailMessage()
        msg['Subject'] = 'OTP Verification'
        msg['From'] = from_email
        msg['To'] = email
        msg.set_content(f"Your OTP is: {otp_code}")

        server.send_message(msg)
        server.quit()
        print("OTP sent to", email)  # Debug: Check if OTP is sent
    except Exception as e:
        print("Failed to send OTP:", e)



if __name__ == '__main__':
    app.run(debug=True)
