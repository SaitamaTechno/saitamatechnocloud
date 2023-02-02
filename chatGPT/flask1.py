from flask import Flask, render_template, request, redirect, session
import random
import smtpmail
import docker
import threading
import qrcode
import sql1

def make_qr(name, wallet):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=4,
    )
    qr.add_data(wallet)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(name)

def sendmaill(email, code):
    smtpmail.sendmaill(email, code)
    return 1

def restart_docker(name):
    docker.con_restart(name)
    return 1

def create_docker(name):
    docker.create_root(name, "123")
    return 1

app = Flask(__name__)
app.secret_key = 'peaceful_world'

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
        if username in [sql1.get_usernames()[i][0] for i in range(len(sql1.get_usernames()))]:
            data=sql1.data_from_username(username)[0]
            if username == data[0] and password == data[1] and data[4] == 1:
                session['username'] = username
                return redirect('/main')
            elif username == data[0] and password == data[1] and data[4] == 0:
                return render_template('login.html', log_msg="Your account is not verified. Click the button below and verify!", verifybutton='''<button type="button" onclick="location.href='/verify/{}'">Verify</button>'''.format(username))
            else:
                return render_template('login.html', log_msg="Username and password does not match!")
    return render_template('login.html')

@app.route('/main', methods=['GET', 'POST'])
def mainn():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            if request.form['submit_button'] == 'Reboot':
                threading.Thread(target=restart_docker, args=(username,)).start()
                return render_template('main.html', username=username, dogecoin_address="mywallet_address", dogecoin=100, reboot_text="Rebooted successfully!")
            elif request.form['submit_button'] == 'Rent a Computer':
                threading.Thread(target=create_docker, args=(username,)).start()
                return render_template('main.html', username=username, dogecoin_address="mywallet_address", dogecoin=100, reboot_text="Your computer created!")
                # Perform send dogecoin action
            elif request.form['submit_button'] == 'My Wallet':
                # Perform send dogecoin action
                return redirect("/wallet")
            elif request.form['submit_button'] == 'Log Out':
                session.pop('username', None)
                return redirect('/login')
        return render_template('main.html', username=username, dogecoin_address="mywallet_address", dogecoin=100)
    return redirect('/login')

@app.route('/wallet', methods=['GET', 'POST'])
def wallet():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            wallet = request.form['wallet']
            return render_template('wallet.html', username=username, dogecoin_address="mywallet_address", dogecoin=100, qrcode='''<div><img src="/static/QR/{}.png" alt="mywallet_address"></div>'''.format(username), success_msg="Transaction is successful!")
        return render_template('wallet.html', username=username, dogecoin_address="mywallet_address", dogecoin=100, qrcode='''<div><img src="/static/QR/{}.png" alt="mywallet_address"></div>'''.format(username))
    return "Bad Request!"
@app.route('/register', methods=['GET', 'POST'])
def register():
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
                threading.Thread(target=sendmaill, args=(email, verification_code,)).start()
                return redirect('/verify/' + username)
            else:
                return render_template('register.html', username_taken="This username is taken!")
    return render_template('register.html')

@app.route('/verify/<username>', methods=['GET', 'POST'])
def verify(username):
    if request.method == 'POST':
        code = request.form['code']
        data=sql1.data_from_username(username)[0]
        if data[0] == username and data[3] == int(code):
            sql1.update_verified(username, 1)
            make_qr("static/QR/{}.png".format(username), "mywallet")
            return render_template('verified.html')
        return "Invalid verification code"
    return render_template('verify.html', username=username)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
