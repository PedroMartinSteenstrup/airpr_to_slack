# Get depedencies
import pandas as pd
import keyring
import requests
import base64
import json
from urllib import request, parse
import sys
from datetime import date
import time

# Set up the automation
wakeup = time.time()

# Get credentials
profile_id = 'YOUR-COMPETITOR-ID'
token = base64.b64encode(keyring.get_password('AirPR','token').encode('utf-8'))
token = 'Bearer ' + keyring.get_password('AirPR','token')

# Create parameters
today = str(date.today())

params = {'from':'2018-04-18',
        'to':'today',
        'per_page':'1'}

# Embedd the authorisation in the header as per OAuth 2.0 AirPR requirement
headers= {"Authorization": token}

# Make the request
r = requests.get('https://analyst.airpr.com/api/v1/profiles/' + profile_id + '/content_items', 
                 params=params, 
                 headers=headers)

# Decode the json
data = r.json()
decoded_data = json.dumps(data)
decoded = json.loads(decoded_data)

# Retrieve the latest id and define stuff
idValue = decoded['content_items'][0]['id']
recorded_id = open('Output.txt', 'r+')

# Define string for the slack message
for x in decoded['content_items']:
    string = {"attachments": [
                {
                    "fallback": x['summary'],
                    "color": "#37517e",
                    "pretext": '  *YOUR-COMPETITOR-NAME* has a new story',
                    "author_name": x['publication'],
                    "author_link": x['host'] ,
                    "author_icon": "",
                    "title": x['title'],
                    "title_link": x['url'],
                    "text": '_'+x['summary']+'_',
                    "fields": [
                        {
                            "title": "Date",
                            "value": x['date'],
                            "short": 'true'
                        },
                        {
                            "title": "Country",
                            "value": x['country'],
                            "short": 'true'
                        }
                    ]
                }
            ]
        }   

# Define posting to a Slack channel
def send_message_to_slack(text):
    post = string
 
    try:
        json_data = json.dumps(post)
        req = request.Request("YOUR-SLACK-INCOMING-WEBHOOK",
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'}) 
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))    
        
# Check if the id is larger than the one stored in the output file, if yes send to slack, if not, pass
while True:
    wakeup += 30 
    print("Calling AirPR"),
    print(decoded),
    
    for line in recorded_id.readlines():
        if idValue > line:
            send_message_to_slack(string)
            print("bingo, message sent!")
# Saving the value retrieved to a text file for the next call
            with recorded_id as text_file:
                print("{}".format(idValue), file=text_file)
                
        else:
            print("I found nothing interesting :(")
    
    
    while time.time() < wakeup:
        time.sleep(1)    
