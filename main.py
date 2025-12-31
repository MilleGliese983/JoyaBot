from mastodon import Mastodon
from threading import Thread
from functions.streamings import LTLlisten, Login

  
if __name__ == "__main__":
    client: Mastodon = Login()
    Thread(target = LTLlisten, args = (client,)).start()
