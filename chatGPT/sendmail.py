from redmail import outlook
import time

def sendmaill(email, code):
	outlook.username = "saitamatechnobot@outlook.com"
	outlook.password = "aGzansicim.7274"

	outlook.send(
	    receivers=[email],
	    subject="Saitama Techno Cloud",
	    text="Verification Code for Saitama Techno Cloud: {}".format(code)
	)

