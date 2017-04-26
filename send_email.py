import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(animal, name, toaddrs):
	fromaddr = 'neaquarium.explorer@gmail.com'
	msg = MIMEMultipart()
	msg['Subject'] = 'Your Aquarium Visit'
	msg['From'] = fromaddr
	msg['To'] = toaddrs
	filename = 'snapshots/IMG'+name+'.png'
	body = "You became an expert on the " + animal + " today!\nVisit the New England Aquarium website to learn more: http://www.neaq.org"
	msg.attach(MIMEText(body, 'plain'))
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