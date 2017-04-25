import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def send_email(animal, name, toaddrs):
	fromaddr = 'neaquarium.explorer@gmail.com'
	msg = MIMEMultipart()
	msg['Subject'] = 'Your Aquarium Visit'
	msg['From'] = fromaddr
	msg['To'] = toaddrs
	filename = 'IMG_me.png'
	fp = open(filename, 'rb')
	img = MIMEImage(fp.read())
	fp.close()
	msg.attach(img)
	username = 'neaquarium.explorer@gmail.com'
	password = 'CMS.634!'
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg.as_string())
	server.quit()

send_email('', '', 'skiinpink@gmail.com')