# airpr_to_slack
Send AirPR's new coverage to a slack channel

AirPR to Slack gets your PR team (and the wider company) closer to press coverage, blog mentions and competitor tracking by constantly providing a feed of news content straight to your team slack's channels.

This version is made for Python 3.

![how_it_looks](https://raw.githubusercontent.com/PedroMartinSteenstrup/airpr_to_slack/blob/master/AirPRtoSlack.JPG)

# Improvement needed
1. At the moment, the script only fetches 1 item at a time, by checking if the id of the latest available article is higher than the previously recorded one. This obviously would fail to fetch all articles in the event that 2 articles were added to the AirPR analyst simultaneously. One possibility would be to record all fetched article id's and have the readlines() go through the full list, and if missing, post content.

2. `<strong>Keyword</strong>` is forwarded in the field 'summary' and doesn't look very neat
