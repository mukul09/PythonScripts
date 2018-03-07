import time
#To get the dekstop notification --> sudo apt install python3-notify2
import notify2
#To get the mobile notification we use TWILIO API
from twilio.rest import Client
#To get the live score from cricbuzz and to install library we use --> pip install pycricbuzz
from pycricbuzz import Cricbuzz


def fun():
	#we enter our Twilio accoundSid and authToken(find it on twilio account settings)
	accountSid 		= "your accoundSid"
	authToken  		= "your authToken"
	# connecting to TWILIO API
	twilioClient	= Client(accountSid, authToken)
	myTwilioNumber 	= "your twilio number"
	destCellPhone 	= "your mobile number"

	#url = "http://synd.cricbuzz.com/j2me/1.0/livematches.xml"
	#to extract the matches 
	cric       		= Cricbuzz()
	details			= cric.matches()

	#To filter out the None objects from details
	details=filter(None, details)
	message="No match in progress"

	for i in details:
		# traversing i
		if 'mchstate' in i:
			if i['mchstate']== 'inprogress':
				id= i['id']
				main=cric.livescore(id)
				ms =main['batting']['score'][0]
				bat1=main['batting']['batsman'][0]
				bat2=main['batting']['batsman'][1]
				message=i['srs']+ "      "+"Format: "+i['type'] +  "\n" + "Score: " +main['batting']['team']+" "+ms['runs'] +'/'+ms['wickets'] +" ("+ms['overs']+")"+"\n" +bat1['name']+":"+bat1['runs']+"("+bat1['balls']+")   "+ bat2['name']+":"+bat2['runs']+"("+bat2['balls']+")"

	#Generates the message
	notify2.init("Live Score")
	# shows notification on out desktop
	notify2.Notification("Match currently in progress:",message).show()
	# sends the notification to our mobile
	#myMessage = twilioClient.messages.create(body = "Match Currently in progress: " + message, from_=myTwilioNumber, to=destCellPhone)
	#shows notification after every 60 seconds
	time.sleep(60)

while True:
	fun()
