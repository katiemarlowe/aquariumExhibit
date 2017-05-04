import smtplib
import codecs
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PIL import Image

def send_email(animal, name, toaddrs):
	fromaddr = 'neaquarium.explorer@gmail.com'
	msg = MIMEMultipart()
	msg['Subject'] = 'Your Aquarium Visit'
	msg['From'] = fromaddr
	msg['To'] = toaddrs
	filename = 'snapshots/IMG'+name+'.png'
	# body = "You became an expert on the " + animal + " today!\nVisit the New England Aquarium website to learn more: http://www.neaq.org"
	# msg.attach(MIMEText(body, 'plain'))
	photo = Image.open(filename, 'r')
	photo = photo.crop((407, 0, 1033, 352))
	logo = Image.open('NEA_logo.png', 'r')
	photo.paste(logo, box=(10, 10), mask=logo)
	photo.save('snapshots/IMG'+name+'LOGO.png')
	fp = open('snapshots/IMG'+name+'LOGO.png', 'rb')
	img = MIMEImage(fp.read())
	fp.close()
	msg.attach(img)
	if animal == "Right Whale":
		html = "whale-email.html"
	elif animal == "Salmon":
		html = "salmon-email.html"
	elif animal == "Rockhopper Penguin":
		html = "penguin-email.html"
	f = codecs.open('email-html/'+html, 'r')
	msg.attach(MIMEText(f.read(), 'html'))
	username = 'neaquarium.explorer@gmail.com'
	password = 'CMS.634!'
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg.as_string())
	server.quit()
