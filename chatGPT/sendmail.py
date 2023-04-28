from redmail import outlook
import time

def sendmaill(email, code):
	outlook.username = "OUTLOOK_MAIL"
	outlook.password = "OUTLOOK_PASSWORD"

	outlook.send(
	    receivers=[email],
	    subject="Saitama Techno Cloud",
	    text="Verification Code for Saitama Techno Cloud: {}".format(code)
	)

