# Get depedencies
import keyring
import requests
import base64
import json
from urllib import request, parse
from datetime import date
import time

# Set up the automation
wakeup = time.time()

# Get credentials
profile_id = 'PROFILE-ID-FOR-REQUEST'
token = base64.b64encode(keyring.get_password('AirPR', 'token').encode('utf-8'))
token = 'Bearer ' + keyring.get_password('AirPR', 'token')

# Create parameters
today = str(date.today())

params = {'from': '2018-04-18',
          'to': 'today',
          'per_page': '1'}

# Embedd the authorisation in the header as per OAuth 2.0 AirPR requirement
headers = {"Authorization": token}

# Make the request
r = requests.get('https://analyst.airpr.com/api/v1/profiles/' + profile_id + '/content_items',
                 params=params,
                 headers=headers)

# Decode the json
data = r.json()
decoded_data = json.dumps(data)
decoded = json.loads(decoded_data)

# Retrieve the latest id
idValue = decoded['content_items'][0]['id']
reach = decoded['content_items'][0]['reach']

# Define string for the slack message
for x in decoded['content_items']:
    string = x['date'] + '  *TransferWise*   ' + x['publication'] + '    ' + x['story_level'] + '    <' + x['url'] + '>\n\n  ' + '_' + x['title'] + '_ \n\n' + '```' + x['summary'] + '```'

# Define posting to a Slack channel
def send_message_to_slack(text):
    post = {"text": "{0}".format(text)}

    try:
        json_data = json.dumps(post)
        req = request.Request("SLACK-INCOMING-WEBHOOK-URL",
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'})
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))

# Check if the id is larger than the one stored in the output file, if yes send to slack, if not, pass

while True:
    wakeup += 30
    print("Calling AirPR"),

    for line in open('Output.txt', 'r').readlines():
        if idValue > line:
            send_message_to_slack(string)
            print("bingo, message sent!")
# Saving the value retrieved to a text file for the next call
            with open("Output.txt", "w") as text_file:
                print("{}".format(idValue), file=text_file)
        else:
            print("I found nothing interesting :(")

    while time.time() < wakeup:
        time.sleep(1)
