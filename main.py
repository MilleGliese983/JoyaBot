from threading import Thread
from functions.streamings import login, listen

def main():
    client = login()
    Thread(target = listen, args = (client,)).start()

if __name__ == "__main__":
    main()
