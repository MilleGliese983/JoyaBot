from mastodon import Mastodon
from threading import Thread
from utils.clients import client
from functions.streamings import LTLlisten, Login


if __name__ == "__main__":
    Thread(target = LTLlisten, args=(client,)).start()
    print("start streaming timeline")