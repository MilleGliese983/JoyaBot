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
    chime_list = [
        "ゴーン",
        "ゴーーン",
        "ゴーーーン",
        "ゴォォォン",
        "ゴーーーン……",
        "ゴーーーん"
    ]
    client.status_reply(
        to_status = status,
        status = random.choice(chime_list)
    )

def countBonnou(client: Mastodon):
    yearstart = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if yearstart.month == 1 and yearstart.day <= 15:
        yearstart.year -= 1
    yearstart = yearstart.replace(month=1, day=15)
    yearend = yearstart.replace(year=yearstart.year+1)

    bonnnou_tag = "煩悩"
    bonnoulist = []
    bonnoulist_page = client.timeline_hashtag(bonnnou_tag, limit=40)
    while len(bonnoulist_page) != 0:
        bonnoulist += bonnoulist_page
        if bonnoulist[-1]['created_at'].replace(tzinfo=None) + timedelta(hours=9) < yearstart:
            break
        last_id = bonnoulist[-1]['id']
        bonnoulist_page = client.timeline_hashtag(bonnnou_tag, max_id=last_id, limit=40)
    
    counter = 0
    for tl in bonnoulist:
        toottime = tl['created_at'].replace(tzinfo=None) + timedelta(hours=9)
        if yearstart <= toottime < yearend:
            counter += 1
    
    client.toot(f"みんなから集まった今年の煩悩は{counter}個です！")