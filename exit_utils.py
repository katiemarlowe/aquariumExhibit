import smtplib
import codecs
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PIL import Image

def save_photo(img_num):
	filename = 'snapshots/IMG'+str(img_num)+'.png'
	photo = Image.open(filename, 'r')
	photo = photo.crop((407, 0, 1033, 352))
	logo = Image.open('NEA_logo.png', 'r')
	photo.paste(logo, box=(10, 10), mask=logo)
	photo.save('snapshots/IMG'+str(img_num)+'LOGO.png')

def send_email(animal, toaddrs, img_num):
	fromaddr = 'neaquarium.explorer@gmail.com'
	msg = MIMEMultipart()
	msg['Subject'] = 'Your Aquarium Visit'
	msg['From'] = fromaddr
	msg['To'] = toaddrs
	fp = open('snapshots/IMG'+str(img_num)+'LOGO.png', 'rb')
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

def send_sms(phone_number, phone_carrier, animal, img_num):
	# extensions = ['@mms.att.net', '@mms.att.net', '@vzwpix.com', '@messaging.sprintpcs.com']
	if phone_carrier == 'AT&T':
		ex = '@mms.att.net'
	elif phone_carrier == 'T-Mobile':
		ex = '@mms.att.net'
	elif phone_carrier == 'Verizon':
		ex = '@vzwpix.com'
	elif phone_carrier == 'Sprint':
		ex = '@messaging.sprintpcs.com'
	fromaddr = 'neaquarium.explorer@gmail.com'
	fp = open('snapshots/IMG'+str(img_num)+'LOGO.png', 'rb')
	img = MIMEImage(fp.read())
	fp.close()
	username = 'neaquarium.explorer@gmail.com'
	password = 'CMS.634!'
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	toaddr = phone_number+ex
	msg = MIMEMultipart()
	msg['Subject'] = 'Your ' + animal + ' selfie!'
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg.attach(img)
	server.sendmail(fromaddr, toaddr, msg.as_string())
	# for ex in extensions:
	# 	toaddr = phone_number+ex
	# 	msg = MIMEMultipart()
	# 	msg['Subject'] = 'Your ' + animal + ' selfie!'
	# 	msg['From'] = fromaddr
	# 	msg['To'] = toaddr
	# 	msg.attach(img)
	# 	server.sendmail(fromaddr, toaddr, msg.as_string())
	server.quit()
	print('text sent to: ', toaddr)
