import smtplib
import email
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

class EmailManager:
	"""
		Manager used to send emails using SMTP
	"""
	def __init__(self):
		self.fromaddr='<FROM EMAIL>'
		self.toaddrs='trigger@ifttt.com'
		self.username='<EMAIL_USERNAME>'
		self.password='<EMAIL_PASSWORD>'

	def sendMsg(self,subject,text):
		# The actual mail send
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(self.username,self.password)

		msg = email.MIMEMultipart.MIMEMultipart()
		msg['Subject'] = subject
		msg['From'] = self.fromaddr
		msg['To'] = self.toaddrs 

 		msg.attach(MIMEText(text))

		server.sendmail(self.fromaddr, self.toaddrs, msg.as_string())
		server.quit()

