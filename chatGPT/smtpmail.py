import smtplib
from email.mime.text import MIMEText

def sendmaill(receiver_email, code):
    sender_email = "stbusiness207@gmail.com"  # Your Gmail address
    password = "usbtgjzjxffloutl"  # Sender's Gmail password
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  # Connect to Gmail's SMTP server
    smtp_server.login(sender_email, password)  # Login to the Gmail account

    message = MIMEText("Saitama Techno Cloud verification code: {}".format(code))  # Create message
    message["Subject"] = "Saitama Techno Cloud"
    message["From"] = sender_email
    message["To"] = receiver_email
    smtp_server.sendmail(sender_email, receiver_email, message.as_string())  # Send the email
#smtp_server.quit()  # Log out of the Gmail account
#sendmaill("halukenestelli143@gmail.com", 123456)
