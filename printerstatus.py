import willie.module
import urllib
import re
import json
import os


@willie.module.commands('printerstatus')
def timeleft(bot, trigger):
	bot.say('Command Recieved')
	url = 'http://ultimaker.local'
	
	jobjson = urllib.urlopen(url + '/api/job')
	
	data = json.load(jobjson)
	state = data['state']

	if state == 'Printing':
		timeleft = data["progress"]["printTimeLeft"]
		timeleft = timeleft/60
		if timeleft > 60:
			timeleft = timeleft/60
			timeleft = str(timeleft)
			timeleft = (timeleft + " Hours.")
		else:
			timeleft = str(timeleft)
			if timeleft > 1:
				timeleft = (timeleft + " Minutes.")
			else:
				timeleft = (timeleft + " Minute.")

		completion = data["progress"]["completion"]
		completion = str(completion)
		name = data['job']["file"]["name"]
		
		bot.say("The ultimaker currently is printing " + name + ". The print is currently at " + completion + "%. The print will complete in roughly " + timeleft)
	else:
		bot.say("The ultimaker is currently not printing anything.")
