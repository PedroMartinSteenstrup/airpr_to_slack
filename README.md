# Onclusive_to_slack
Send Onclusive's new coverage to a slack channel

Onclusive to Slack gets your PR team (and the wider company) closer to press coverage, blog mentions and competitor tracking by constantly providing a feed of news content straight to your team slack's channels.

This version is made for Python 3.

![how_it_looks](https://github.com/PedroMartinSteenstrup/airpr_to_slack/blob/master/AirPRtoSlack.JPG?raw=true)

# What it does
1. Query the latest article available on Onclusive's API every X seconds (triggered by CRON on server)
2. Check it against previously store list of IDs in PostgreSQL
3. Post content to slack channel if deemed relevant

# What it doesn't do (and should)
1. If two or more article are added simultaneously on Onclusive's platform, only most recent one will be picked up. Ideally it should be able to handle several newly added articles, not just the most recent one.

# Stuff it needs to run without change
1. PostgreSQL and a table like reports.slack_press_hits with 2 columns (id, provider)
2. Server environment on Python 3
3. Well, most importantly, a service contract with AirPR
