import json
import os
import datetime
import requests

import dateutil.parser
import dateutil.utils
import dateutil.tz


events = [
    {
        "date": "2019-08-31 12:00:00 -0500"
    }
]

# Just add in the 3 components of the Slack webhook URL: team, channel, secret token
SLACK_WEBHOOK_TOKEN = os.getenv("SLACK_WEBHOOK_TOKEN", None)
SLACK_URL = "https://hooks.slack.com/services/%s" % SLACK_WEBHOOK_TOKEN

text = None
for event in events:
    dflt_tz = dateutil.tz.tzoffset("EST", -18000)
    today = dateutil.utils.today(dflt_tz)
    d = dateutil.parser.parse(event['date']) - today
    if d.days < 0:
        continue # go to next event
    elif d == 0:
        text = "The man burns tonight! Hopefully no one is reading this."
    elif d == 1:
        text = "The man burns tomorrow!"
    else:
        text = "The man burns in %s days." % (d.days)

    break

payload = {
    "username": "BurnBot",
    "text": text,
    "icon_emoji": ":fire:"
}

print("Sending Payload:")
print(json.dumps(payload, sort_keys=True))

if text is not None and SLACK_WEBHOOK_TOKEN is not None:
    requests.post(SLACK_URL, json = payload)