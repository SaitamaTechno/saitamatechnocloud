from flask import Flask, render_template, request, redirect, session
import random
import smtpmail
import docker
import threading
import qrcode
import sql1
import datetime
import dogecoin_testnet as doge

def get_date():
    date=datetime.datetime.now()
    mystr=str(date.year)+"/"+ str(date.month)+ "/" + str(date.day)
    return mystr

def hide_email(email):
    secret_email=""
    n2=email.find("@")
    for i in range(len(email)):
        if 0 < i < n2-1:
            secret_email+="*"
        else:
            secret_email+=email[i]
    return secret_email


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

def create_docker(name, password):
    hostlist=docker.create_root(name, password)
    sql1.update_ports(name, str(hostlist))
def delete_docker(name):
    docker.delete_docker(name)

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
                return render_template('login.html', log_msg="Username and password does not match!", verifybutton='''<button type="button" onclick="location.href='/change_pass_email/{}'">Forgot Your Password?</button>'''.format(username))
    return render_template('login.html')

@app.route('/main', methods=['GET', 'POST'])
def mainn():
    if 'username' in session:
        username = session['username']
        wallet_info = doge.get_wallet_info(username)
        wallet_address = wallet_info["address"]
        wallet_balance = wallet_info["available_balance"]
        if request.method == 'POST':
            if request.form['submit_button'] == 'My Computers':
                return redirect("/pc_table")
            elif request.form['submit_button'] == 'My Wallet':
                return redirect("/wallet")
            elif request.form['submit_button'] == 'Log Out':
                session.pop('username', None)
                return redirect('/login')
        return render_template('main.html', username=username, dogecoin_address=wallet_address, dogecoin=wallet_balance)
    return redirect('/login')

@app.route('/rent_pc', methods=['GET', 'POST'])
def rent_pc():
    if 'username' in session:
        username = session['username']
        wallet_info = doge.get_wallet_info(username)
        available_balance = wallet_info["available_balance"]
        if request.method == 'POST':
            password = request.form['password']
            verify_password = request.form['verify_password']
            computer_name = request.form['computer_name']
            disk_size = request.form['disk_size']
            if password != verify_password:
                # code to return an error message if the passwords don't match
                return render_template('rent_pc.html', msg="Passwords do not match!")
                pass
            else:
                if computer_name not in docker.get_names():
                    try:
                        if username != sql1.data_from_username_pc(username)[0][0]:
                            pass
                    except IndexError:
                        if int(disk_size)*2 < float(available_balance):
                            threading.Thread(target=doge.send_money, args=(str(int(disk_size)*2), username, "default",)).start()
                            sql1.create_pc(username, computer_name, int(disk_size), int(disk_size)*2, "active", get_date())
                            threading.Thread(target=create_docker, args=(computer_name, password,)).start()
                            return render_template('rent_pc.html', msg="Computer successfully created! Please check PC Table!", money=available_balance+" Doge")
                        else:
                            return render_template('rent_pc.html', msg="You don't have enough money!", money=available_balance+" Doge")
                    else:
                        return render_template('rent_pc.html', msg="Each user can have only 1 computer!", money=available_balance+" Doge")
                else:
                    return render_template('rent_pc.html', msg="This computer name is taken!", money=available_balance+" Doge")
        return render_template("rent_pc.html", money=available_balance+" Doge")
    return redirect("/login")
@app.route('/pc_table', methods=['GET', 'POST'])
def pc_table():
    if 'username' in session:
        username = session['username']
        try:
            data=sql1.data_from_username_pc(username)[0]
            name=data[1]
            try:
                portlist=[int(i) for i in data[2].replace("[", "").replace("]", "").split(", ")]
            except AttributeError:
                return render_template("pc_table.html", username=username, msg="Please wait a minute and Refresh the page. Your computer is still in progress!")
            sshport=portlist[0]
            portlist.pop(0)
            availableports=portlist
            disk_size=str(data[3])
            disk_size=docker.get_size_from_name(name)+"/"+disk_size
            doge=data[4]
            status=data[5]
            if request.method == 'POST':
                button = request.form['submit_button']
                if button == "Reboot":
                    threading.Thread(target=restart_docker, args=(name,)).start()
                    return render_template("pc_table.html", username=username, name=name, sshport=sshport, availableports=availableports, disk_size=str(disk_size)+"GB", doge=str(doge)+" Doge", status=status, msg="Successfully Rebooted!")
                elif button == "Delete":
                    sql1.delete_user_pc(name)
                    threading.Thread(target=delete_docker, args=(name,)).start()
                    return render_template("pc_table.html", username=username, msg="Computer deleted!")
            return render_template("pc_table.html", username=username, name=name, sshport=sshport, availableports=availableports, disk_size=str(disk_size)+"GB", doge=str(doge)+" Doge", status=status)
        except IndexError:
            return render_template("pc_table.html", username=username)
    return redirect('/login')

@app.route('/wallet', methods=['GET', 'POST'])
def wallet():
    if 'username' in session:
        username = session['username']
        wallet_info = doge.get_wallet_info(username)
        wallet_address = wallet_info["address"]
        wallet_balance = wallet_info["available_balance"]
        wallet_pending = wallet_info["pending_received_balance"]
        if request.method == 'POST':
            wallet = request.form['wallet']
            doge_quantity = float(request.form['doge_quantity'])
            if doge_quantity < float(wallet_balance) and doge_quantity >= 0.03:
                if request.form["submit_button"]=="Send Doge":
                    threading.Thread(target=doge.send_money_to_address, args=(str(doge_quantity), username, wallet,)).start()
                    #doge.send_money_to_address(str(doge_quantity), username, wallet)
                    return render_template('wallet.html', username=username, dogecoin_address=wallet_address, dogecoin_available=wallet_balance, dogecoin_pending=wallet_pending, qrcode='''<div><img src="/static/QR/{}.png" alt="mywallet_address"></div>'''.format(username), success_msg="Transaction is successful!")
                elif request.form["submit_button"]=="Calculate Fee":
                    fee = doge.calculate_address_fee(str(doge_quantity), username, wallet)
                    return render_template('wallet.html', username=username, dogecoin_address=wallet_address, dogecoin_available=wallet_balance, dogecoin_pending=wallet_pending, qrcode='''<div><img src="/static/QR/{}.png" alt="mywallet_address"></div>'''.format(username), success_msg="Transaction Fee is {} Doge".format(fee))
            elif doge_quantity < float(wallet_balance) and doge_quantity <= 0.03:
                return render_template('wallet.html', username=username, dogecoin_address=wallet_address, dogecoin_available=wallet_balance, dogecoin_pending=wallet_pending, qrcode='''<div><img src="/static/QR/{}.png" alt="mywallet_address"></div>'''.format(username), success_msg="Doge quantity cannot be less than 0.03")
            else:
                return render_template('wallet.html', username=username, dogecoin_address=wallet_address, dogecoin_available=wallet_balance, dogecoin_pending=wallet_pending, qrcode='''<div><img src="/static/QR/{}.png" alt="mywallet_address"></div>'''.format(username), success_msg="You don't have enough money!")
        return render_template('wallet.html', username=username, dogecoin_address=wallet_address, dogecoin_available=wallet_balance, dogecoin_pending=wallet_pending, qrcode='''<div><img src="/static/QR/{}.png" alt="mywallet_address"></div>'''.format(username))
    return redirect('/login')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        if password != verify_password:
            # code to return an error message if the passwords don't match
            return render_template('register.html', msg="Passwords do not match!")
            pass
        #elif email in [sql1.get_emails()[i][0] for i in range(len(sql1.get_emails()))]:
        #    return render_template('register.html', username_taken="This email has already registered!")
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

@app.route('/change_pass_email/<username>', methods=['GET', 'POST'])
def change_pass_email(username):
    data = sql1.data_from_username(username)[0]
    email = data[2]
    newemail = hide_email(email)
    if request.method == 'POST':
        if request.form['submit_button'] == 'Yes':
            if data[5] == 190719071907:
                verification_code = random.randint(100000, 999999)
                sql1.update_forgot_pass(username, verification_code)
                threading.Thread(target=sendmaill, args=(email, verification_code,)).start()
                return redirect('/change_pass/{}'.format(username))
            else:
                return render_template("change_pass_email.html", username=username, email=newemail, msg="We have already sent the code, please check your Spam section. And click the button below to verify your code!", but='''<button type="button" onclick="location.href='/change_pass/{}'">Verify</button>'''.format(username))
    return render_template("change_pass_email.html", username=username, email=newemail)
@app.route('/change_pass/<username>', methods=['GET', 'POST'])
def change_pass(username):
    if request.method == 'POST':
        code = request.form['code']
        password = request.form['password']
        verify_password = request.form['verify_password']
        if password != verify_password:
            # code to return an error message if the passwords don't match
            return render_template("change_pass.html", username=username, log_msg="Passwords do not match!")
            pass
        else:
            data = sql1.data_from_username(username)[0]
            if data[0] == username and data[5] == int(code):
                sql1.change_password(username, password)
                sql1.update_forgot_pass(username, 190719071907)
                return render_template('changed_pass.html')
            else:
                return render_template("change_pass.html", username=username, log_msg="Your code is wrong!")
    return render_template("change_pass.html", username=username)
@app.route('/verify/<username>', methods=['GET', 'POST'])
def verify(username):
    if request.method == 'POST':
        code = request.form['code']
        data = sql1.data_from_username(username)[0]
        if data[0] == username and data[3] == int(code):
            sql1.update_verified(username, 1)
            doge.create_new_wallet(username)
            wallet=doge.get_wallet_info(username)["address"]
            make_qr("static/QR/{}.png".format(username), wallet)
            return render_template('verified.html')
        return "Invalid verification code"
    return render_template('verify.html', username=username)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
