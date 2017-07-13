import os
import sys
import argparse
import itertools
import irc.client

from ascii_converter import *
from image_finder import *

''' Picascii is an IRC bot which displays pixel art for the specified search terms. '''

image_width = 100
target = None

def on_connect(connection, event):
    if irc.client.is_channel(target):
        connection.join(target)
        return
    main_loop(connection)

def on_join(connection, event):
    main_loop(connection)

def on_disconnect(connection, event):
    raise SystemExit()

# Send a message to the target.
def send(message, connection=None):
    if connection:
        connection.privmsg(target, message)
    else:
        print message

# Continuously read lines from standard input.
def get_lines():
    while True:
        yield sys.stdin.readline().strip()

# Main loop for the bot - process incoming messages.
def main_loop(connection=None):
    global image_width
    for line in itertools.takewhile(bool, get_lines()):
        tokens = line.split(' ')
        command = tokens[0]
        if command == 'show':
            if len(tokens) > 1:
                img = find_image(tokens[1:])
                if img:
                    temp = "temp.jpg"
                    download_image(img, temp)
                    send(image_to_ascii(temp, image_width, " .,:;ox%#@"), connection)
                    os.remove(temp)
                else:
                    send("No matching images found!", connection)
            else:
                send("Err... you forgot to add search terms!", connection)
        elif command == 'size':
            if len(tokens) == 2:
                image_width = int(tokens[1])
            else:
                send("You must specify an integer size!", connection)
        elif command == 'quit':
            break

# Parse command line arguments.
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('server')
    parser.add_argument('target', help="a nickname or channel")
    parser.add_argument('-p', '--port', default=6667, type=int)
    return parser.parse_args()

# Main entry point - open connection if possible else enter offline mode.
def main():
    global target

    bot_nick = "picascii"
    args = get_args()

    target = args.target

    online = True
    reactor = irc.client.Reactor()
    try:
        c = reactor.server().connect(args.server, args.port, bot_nick)
    except irc.client.ServerConnectionError:
        print "Unable to connect: "
        print sys.exc_info()[1]
        print "Running offline..."
        online = False

    if online:
        c.add_global_handler("welcome", on_connect)
        c.add_global_handler("join", on_join)
        c.add_global_handler("disconnect", on_disconnect)
        reactor.process_forever()
    else:
        main_loop()

if __name__ == '__main__':
    main()
