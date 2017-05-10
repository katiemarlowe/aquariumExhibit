import smtplib
import codecs
from twilio.rest import Client
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

# Your Account SID from twilio.com/console
account_sid = "AC0efdfe0d5464098a719c5e5f83ea97bb"
# Your Auth Token from twilio.com/console
auth_token  = "f4eff994c2687cd3b8de4ac0b4636e79"

client = Client(account_sid, auth_token)

def send_sms(phone_number, animal):
	message = client.messages.create(
	    to='+1'+phone_number, 
	    from_="+16466815119",
	    body="Thanks for visiting the New England Aquarium! Show this message to the gift shop to receive 30% off a "+animal+" souvenir.")