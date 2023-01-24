from flask import Flask, render_template, request, redirect
import smtplib
import random
from sendmail import sendmaill
import sql1

app = Flask(__name__)
#app.secret_key = 'secretkey'

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # code to check if the user exists in the database
        # and if the password is correct
        return redirect('/')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        if password != verify_password:
            # code to return an error message if the passwords don't match
            pass
        else:
            # code to add the user to the database
            verification_code = random.randint(100000, 999999)
            # code to send an email with the verification code
            with open("data/verify.txt", "a") as f:
                f.write(username + "," + str(verification_code) + "\n")
            sendmaill(email, verification_code)
            return redirect('/verify/'+username)
    return render_template('register.html')

@app.route('/verify/<username>', methods=['GET', 'POST'])
def verify(username):
    if request.method == 'POST':
        code = request.form['code']
        with open("data/verify.txt", "r") as f:
            datalist = f.readlines()
            for line in datalist:
                data = line.strip().split(",")
                if data[0] == username and data[1] == code:
                    return render_template('verified.html')
        return "Invalid verification code"
    return render_template('verify.html', username=username)


if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.144", port=2000)
