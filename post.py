import json
import os
import requests

import dateutil.parser
import dateutil.utils
import dateutil.tz


events = [{
    "date": "2024-08-31 08:00:00 -0800"
}]

SLACK_WEBHOOK_TOKEN = os.getenv("SLACK_WEBHOOK_TOKEN", None)
SLACK_URL = "https://hooks.slack.com/services/%s" % SLACK_WEBHOOK_TOKEN

text = None
for event in events:
    dflt_tz = dateutil.tz.tzoffset("EST", -18000)
    today = dateutil.utils.today(dflt_tz)
    d = dateutil.parser.parse(event['date']) - today

    print(f"Days remaining: {d.days}")

    if d.days < 0:
        continue  # go to next event
    elif d.days == 0:
        text = "The man burns tonight! Hopefully no one is reading this."
    elif d.days == 1:
        text = "The man burns tomorrow!"
    elif d.days < 45 or d.days % 7 == 0:
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
    requests.post(SLACK_URL, json=payload)
