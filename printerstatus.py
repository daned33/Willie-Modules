
# The MIT License (MIT)

# Copyright (c) 2015 daned33(Daniel Edwards)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# load up the modules
import willie.module
import urllib
import re
import json
import os


@willie.module.commands('printerstatus')  # run the script on the command '.printerstatus'
def timeleft(bot, trigger):
	url = 'http://ultimaker.local'
	
	jobjson = urllib.urlopen(url + '/api/job')  # Grab json job data from the Octoprint API 
	
	data = json.load(jobjson) # load the raw json code so that the json module understands the data
	
	state = data['state'] # set the 'state' variable as what is grabbed from the API (Printing for printing, Operational for idle.)

	if state == 'Printing':    # if the printer is printing, it will grab extra data and post a status onto the IRC.
	
		timeleft = data["progress"]["printTimeLeft"] # parse the time left (in seconds) from the json data
		timeleft = timeleft/60                       # convert seconds to minutes
		if timeleft > 60:                            # check if it's needed to be converted to hours
			timeleft = timeleft/60                   # convert minutes to hours
			timeleft = str(timeleft)                 # turn the time interger into a string
			timeleft = (timeleft + " Hours.")        # add the 'Hours.' string to the time into a variable to create a single unit e.g. (1.3 hours)
		else:                                        # if the time left is 60 minutes or left, print Minute(s) behind instead.
			timeleft = str(timeleft)                
			if timeleft > 1:                         # if over one minute, then it will be minute instead.
				timeleft = (timeleft + " Minutes.")
			else:
				timeleft = (timeleft + " Minute.")

		completion = data["progress"]["completion"]  # check percent completion from the json data
		completion = str(int(completion)             # convert to an interger then string and save as the variable 'completion'
		
		name = data['job']["file"]["name"]           # grab the name of the file that is currently printing from the json data
		

		# this is what will be printed into the IRC chat
		bot.say("The ultimaker currently is printing " + name + ". The print is currently at " + completion + "%. The print will complete in roughly " + timeleft)
	else:
		bot.say("The ultimaker is currently not printing anything.") # if there is nothing currently printing, it will print this to the IRC
