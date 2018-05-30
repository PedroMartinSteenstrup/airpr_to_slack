# Get depedencies
import keyring
import requests
import json
from urllib import request
from datetime import date
import time

# Define posting to a Slack channel
def send_message_to_slack(text):
    post = string

    try:
        json_data = json.dumps(post)
        req = request.Request("https://hooks.slack.com/services/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",
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'})
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))


while True:
    today = str(date.today())

    wakeup = time.time()
    today = str(date.today())
    params = {'from': '2018-04-18',
              'to': 'today',
              'per_page': '1'}
    profile_id = '3213'
    token = 'Bearer ' + keyring.get_password('AirPR', 'token')
    headers = {"Authorization": token}

    r = requests.get('https://analyst.airpr.com/api/v1/profiles/' + profile_id + '/content_items',
                     params=params,
                     headers=headers)
    print("Calling AirPR")

    data = r.json()
    decoded_data = json.dumps(data)
    decoded = json.loads(decoded_data)
    print("decode data")
    idValue = decoded['content_items'][0]['id']
    print("retrieving_id"),

    for x in decoded['content_items']:
        string = {"attachments": [
            {
                "fallback": x['summary'],
                "color": "#37517e",
                "pretext": '  *TransferWise* has a new story',
                "author_name": x['publication'],
                "author_link": x['host'],
                "author_icon": "",
                "title": x['title'],
                "title_link": x['url'],
                "text": '_' + x['summary'] + '_',
                "fields": [
                    {
                        "title": "Level",
                        "value": x['story_level'],
                        "short": 'true'
                    },
                    {
                        "title": "Date",
                        "value": x['date'],
                        "short": 'true'
                    },
                    {
                        "title": "Country",
                        "value": x['country'],
                        "short": 'true'
                    },
                    {
                        "title": "Message",
                        "value": x['messages'],
                        "short": 'true'
                    }
                ]
            }
        ]
        }
    with open('Output.txt', 'r+') as fobj:
        textc = fobj.read().strip().split()
        try:
            s = idValue
            if s in textc:
                print("Matched, ignoring article")
            else:
                fobj.write("\n" + idValue)
                send_message_to_slack(string)
                print("sending message to slack")
        except Exception as e:
            print("There was an error and the script stopped running")

    time.sleep(20)
