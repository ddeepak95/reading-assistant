import requests
import json

def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/mg.ddeepak95.com/messages",
		auth=("api", "0173dbac13bb376cd6dc7dbb607f12ac-623e10c8-f26c6909"),
		data={"from": "Excited User <noreply@mg.ddeepak95.com>",
			"to": ["ddeepak95@gmail.com"],
			"subject": "Hello",
			"text": "Testing some Mailgun awesomeness!"})

send = send_simple_message()

print(json.dumps(send.json(), indent=4, sort_keys=True))