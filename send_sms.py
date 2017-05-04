from twilio.rest import Client

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