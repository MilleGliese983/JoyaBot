from schemas.status import Status
from mastodon import Mastodon, StreamListener
from datetime import datetime
import time
import re
from utils.load_env import APPTYPE, INSTANCE_URL, ACCESS_TOKEN
from .functions import get_name, rewrite, deleteBonnou, countBonnou


class Bot(StreamListener):
    def __init__(self, client: Mastodon):
        super(Bot, self).__init__()
        self.client = client

    def on_update(self, status: Status):
        get_status = status
        get_status['content'] = rewrite(get_status['content'])
        print(datetime.now())
        print(f"==={get_name(get_status['account'])}======\n{get_status['content']}\n\n")

        if get_status['account']['bot'] or get_status['reblog'] != None:
            return

        if re.search((r'#煩悩.+'), get_status['content']):
            deleteBonnou(self.client, get_status)
            return
        
        if re.search((r'煩悩.*数'), get_status['content']):
            countBonnou(self.client)
            return


        
def Login() -> Mastodon:
    mastodon = Mastodon(
        access_token = ACCESS_TOKEN,
        api_base_url = INSTANCE_URL
    )

    if APPTYPE == 'DEV':
        mastodon.session.verify = False # 実装するときは書かない
    return mastodon

def LTLlisten(client: Mastodon):
    bot = Bot(client)
    while True:
        try:
            client.stream_local(bot, timeout=50000)
        except Exception as e:
            print(datetime.now())
            print(e)
            time.sleep(60)
