#!/usr/bin/env python3
# coding: utf-8

# Get dependencies
import keyring
import requests
import json
from datetime import date
import datetime
import sys
import psycopg2

# Define a few stuff
db_password = keyring.get_password('YOUR_STUFF_HERE', 'YOUR_STUFF_HERE')
provider = "YOUR_COMPETITOR"


# posting to a Slack channel
def slackit():
    webhook_url = 'YOUR_WEBHOOK_URL'
    slack_data = string
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    insert_id()


# checking if ID in the API call matches an existing stored id
def check_id():
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM reports.slack_press_hits WHERE provider = 'YOUR_COMPETITOR' ORDER BY id DESC LIMIT 5")
        result = cur.fetchall()[0]
        if int(result[0]) == int(idValue):
            cur.close()
            conn.close()
            pass
        else:
            filter_result()
    except OSError:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except:
        print("Unexpected error:", sys.exc_info()[0])


# filtering if the content is relevant, you can tweak that as you wish
def filter_result():
    if reach < 500000:
        insert_id()
    elif country == 'United States' and reach < 1500000:
        insert_id()
    elif country == 'United Kingdom' and reach < 1000000:
        insert_id()
    elif country == 'Spain' and reach < 1000000:
        insert_id()
    elif country == 'Germany' and reach < 1000000:
        insert_id()
    elif country == 'France' and reach < 1000000:
        insert_id()
    elif country == 'Japan' and reach < 1000000:
        insert_id()
    elif country == 'Poland' and reach < 1000000:
        insert_id()
    elif country == 'Italy' and reach < 1000000:
        insert_id()
    elif country == 'Estonia' and reach < 500000:
        insert_id()
    elif country == 'Russian Federation' and reach < 1000000:
        insert_id()
    else:
        slackit()


# storing the ID in the db
def insert_id():
    cur = conn.cursor()
    inserts = "INSERT INTO reports.slack_press_hits (id, provider) VALUES (%s, %s);"
    data_inserts = (idValue, provider)
    cur.execute(inserts, data_inserts)
    cur.close()
    conn.close()
    
    
try:
    to_date = str(date.today())
    from_date = str(date.today() - datetime.timedelta(1))
    params = {'from': from_date,
              'to': to_date,
              'per_page': '1',
              'sort': "date"}
    profile_id = 'YOUR_PROFILE_ID_ON_AIRPR'
    token = 'Bearer ' + keyring.get_password('YOUR_STUFF_HERE', 'YOUR_STUFF_HERE')
    headers = {"Authorization": token}
    r = requests.get('https://analyst.airpr.com/api/v1/profiles/' + profile_id + '/content_items',
                     params=params,
                     headers=headers)
    conn = psycopg2.connect(database='YOUR_DATABASE',
                            user='YOUR_DB_USERNAME',
                            password=db_password,
                            host='YOUR_HOST',
                            port=YOUR_PORT)
    conn.set_session(autocommit=True)

    decoded = json.loads(json.dumps(r.json()))
    idValue = decoded['content_items'][0]['id']
    reach = format(decoded['content_items'][0]['reach'], ",")
    country = decoded['content_items'][0]['country']
    summary = decoded['content_items'][0]['summary']
    summary = summary.replace("<strong>", "*")
    summary = summary.replace("</strong>", "*")
    author_name = decoded['content_items'][0]['publication']
    author_link = decoded['content_items'][0]['host']
    title = decoded['content_items'][0]['title']
    title_link = decoded['content_items'][0]['url']
    pub_type = decoded['content_items'][0]['type']
    pub_date = decoded['content_items'][0]['date']
    pub_lang = decoded['content_items'][0]['language']
    string = {"attachments": [
            {
                "fallback": decoded['content_items'][0]['summary'],
                "color": "#05FCFF",
                "pretext": '  *YOUR_COMPETITOR* has a new story',
                "author_name": author_name,
                "author_link": author_link,
                "author_icon": "",
                "title": title,
                "title_link": title_link,
                "text": '_' + summary + '_',
                "fields": [
                    {
                        "title": "Language",
                        "value": ':' + pub_lang + ':',
                        "short": 'true'
                    },
                    {
                        "title": "Date",
                        "value": pub_date,
                        "short": 'true'
                    },
                    {
                        "title": "Country",
                        "value": country,
                        "short": 'true'
                    },
                    {
                        "title": "Reach",
                        "value": reach,
                        "short": 'true'
                    }
                        ]
            }
                            ]
              }

    try:
        check_id()
    except OSError:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
except Exception as e:
    print(e)
