
import asyncio

from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl import functions, types
from telethon import events

import os, re, sys
import argparse
import string
import pathlib


parser = argparse.ArgumentParser()
parser.add_argument(
    '--gn',
    type=str, 
    help='tg group name'
)
parser.add_argument(
    '--u',
    type=str, 
    help='tg user',
    default='r3pt1101d'
)
parser.add_argument(
    '--msg',
    type=str, 
    help='tg message to --tgu'
)
parser.add_argument(
    '--img',
    type=pathlib.Path,
    help='path to a file'
)

args = parser.parse_args()

if args.u is None:
    parser.print_help()

# https://github.com/goq/telegram-list?tab=readme-ov-file
APP_ID = 24436001
APP_HASH = ''
TOKEN = ':'
PHONE = '+'
session_name = 'test'
THIS_SCRIPT_DIR = 'G:/Desktop/py/TG'

client = TelegramClient(
    session_name, 
    APP_ID, 
    APP_HASH
)

client.start()

async def send_a_message(): 
    async with client:
        await client.send_message(args.u, args.msg)

# https://medium.com/@kokhua81/how-to-send-messages-and-files-to-telegram-with-python-66c1abeea7a6
async def send_a_pic(): 
    async with client:
        await client.send_file(args.u, args.img) 

@client.on(events.NewMessage)
async def reply_to_a_message(event):
    await event.reply(event.text.reversed())

@client.on(events.NewMessage)
async def respond_to_a_message(event):
    await event.respond(event.text.reversed())


def main():
    loop = asyncio.get_event_loop()
    client.add_event_handler(reply_to_a_message)
    client.add_event_handler(respond_to_a_message)

    try:
        if (args.u and args.msg):
            loop.run_until_complete(send_a_message())
        if args.img:
            loop.run_until_complete(send_a_pic())
    finally:
        with client:
            client.run_until_disconnected()
    

if __name__ == '__main__':
    main()
