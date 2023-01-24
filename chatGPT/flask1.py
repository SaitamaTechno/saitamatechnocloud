from flask import Flask, render_template, request, redirect
import smtplib
import random
from sendmail import sendmaill
#import sql1

app = Flask(__name__)
#app.secret_key = 'secretkey'

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    import sql1
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # code to check if the user exists in the database
        # and if the password is correct
        if username in [sql1.get_usernames()[i][0] for i in range(len(sql1.get_usernames()))]:
            data=sql1.data_from_username(username)[0]
            if username == data[0] and password == data[1] and data[4] == 1:
                return "Successfully logged in!"
            elif username == data[0] and password == data[1] and data[4] == 0:
                return "Your account is not verified. Please enter your verification code!"
            else:
                return "Your password is wrong!"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    import sql1
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        if password != verify_password:
            # code to return an error message if the passwords don't match
            return "Passwords do not match!"
            pass
        else:
            # code to add the user to the database
            verification_code = random.randint(100000, 999999)
            # code to send an email with the verification code
            if username not in [sql1.get_usernames()[i][0] for i in range(len(sql1.get_usernames()))]:
                sql1.create_user(username, password, email, verification_code, 0)
                sendmaill(email, verification_code)
                return redirect('/verify/' + username)
            else:
                return "This username is taken!"
    return render_template('register.html')

@app.route('/verify/<username>', methods=['GET', 'POST'])
def verify(username):
    import sql1
    if request.method == 'POST':
        code = request.form['code']
        data=sql1.data_from_username(username)[0]
        if data[0] == username and data[3] == int(code):
            sql1.update_verified(username, 1)
            return render_template('verified.html')
        return "Invalid verification code"
    return render_template('verify.html', username=username)

if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.144", port=2000)
