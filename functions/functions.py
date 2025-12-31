from schemas.status import Status, User
from mastodon import Mastodon
from mastodon.return_types import Status
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import re
import random

def get_name(account: User):
    if len(account['display_name']) == 0:
        return account['username']
    else:
        return account['display_name']

def rewrite(text: str, doRet: bool = True):
    if doRet:
        text = text.replace('</p><p>', '\n\n')
        text = text.replace('<br />','\n')
    else:
        text = text.replace('</p><p>', ' ')
        text = text.replace('<br />',' ')
    text = BeautifulSoup(text, 'html.parser').get_text()
    text = text.replace('&apos;', '\'')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '\"')
    return text

def deleteBonnou(client: Mastodon, status: Status):
    client.status_reply(status, "ゴーン")

def countBonnou(client: Mastodon, status: Status):
    bonnoulist = client.timeline_hashtag("煩悩")
    yearstart = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if yearstart.month == 1 and yearstart.day <= 15:
        yearstart.year -= 1
    yearstart = yearstart.replace(month=1, day=15)
    yearend = yearstart.replace(year=year+1)

    counter = 0
    for tl in bonnoulist:
        toottime = tl['created_at'].replace(tzinfo=None) + timedelta(hours=9)
    if yearstart <= toottime < yearend:
        counter += 1
    
    client.toot(f"みんなから集まった今年の煩悩は{counter}個です！")