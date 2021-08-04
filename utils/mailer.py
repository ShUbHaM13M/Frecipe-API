import smtplib, ssl
from typing import Dict
from config import Settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

settings = Settings()
port = 465
context = ssl.create_default_context()

def send_mail(sender_email: str, recipient: str, mail: Dict[str, str]) -> None:
	"""Function to send mail"""

	if mail['Subject'] == None: raise Exception('Subject not provided.')

	message = MIMEMultipart('alternative')
	message['Subject'] = mail['Subject']
	message['From'] = sender_email
	message['To'] = recipient

	part1 = MIMEText(mail['text'], 'plain')
	message.attach(part1)
	if 'html' in mail.keys() and (html := mail['html']) != None:
		message.attach(
			MIMEText(html, 'html')
		)

	with smtplib.SMTP_SSL(settings.SMTP_CLIENT, port, context=context) as server:
		server.login(settings.MAIL_ACCOUNT, settings.MAIL_PASS)
		server.sendmail(sender_email, recipient, message.as_string())

if __name__ == '__main__':
	send_mail(
		'shubham.heeralal@gmail.com', 
		'pokemon@mail.com', 
		{
			'Subject': 'test', 
			'text': 'have fun ❣', 
			'html': '<b><ul>have fun ❣<ul><b>'
		}
	)