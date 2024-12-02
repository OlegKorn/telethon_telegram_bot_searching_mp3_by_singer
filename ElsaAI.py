from telethon import TelegramClient, events
from telethon.tl.custom import Button
from telethon.errors.rpcerrorlist import FloodWaitError

import logger
from logger import CMDColorLogger, cmd_message_colorized

import asyncio
import os, re, sys
import config 

import muzfondsaver
from muzfondsaver import MuzofondMusicSaver


def main():
    try:
        bot_client = TelegramClient(
            # config.SESSION_NAME,
            None, 
            config.API_ID, 
            config.API_HASH
        )
        bot_client.start(bot_token=config.PrincessElsaAIBot_BOT_TOKEN)
    
        # Handler for the /start command
        @bot_client.on(events.NewMessage(pattern='/start'))
        async def respond_start(event):
            await event.respond(
                'Hello!\nThis bot will send you a chosen song' \
                '(mp3 file) from a list of musician songs' \
                'on muzofond.fm', 
                buttons=[ 
                    Button.inline('Choose a music artist name...')
                ]
            )
        '''
        @bot_client.on(events.CallbackQuery(data=b'Choose a music artist name...'))
        async def handler(event):
            await event.respond(f'Input a name of musician. After that the bot will send the list of tracks of the chosen musician...' )

        # ------------------------------------------------------------------------------------------------------
        @bot_client.on(events.NewMessage(incoming=True))
        async def handler(event):
            event.text = event.text.strip()

            # not /start
            if ('/' not in event.text) and ('start' not in event.text):
                if not any(x.isalpha() for x in event.text):
                    await event.respond('Your musician\'s name didn\'t have any letters! Is it a joke? Try again with a real name...')

                else:
                    cmd_message_colorized(CMDColorLogger(), f'You chose: {event.text}', config.YELLOW)
                    
                    await event.respond(f'You choose: {event.text}')
                    await event.respond(f'Being processed...')

                    mfs = MuzofondMusicSaver(event.text)
                    songs = mfs.get_mp3s_of_author_found_songs()
                    
                    for song in songs:
                        mp3_title = song.split(":::")[1]
                        mp3_link = song.split(":::")[0]
                        print(mp3_link)

                        await event.respond(
                            f'{mp3_link} - {mp3_title}',
                            buttons=[
                                Button.inline(
                                    'Download', 
                                    data='mp3_link'
                                )
                            ]
                        )

        '''
        with bot_client:
            bot_client.run_until_disconnected()

    except FloodWaitError as ex:
        #print('Wait 3600 seconds')
        cmd_message_colorized(CMDColorLogger(), f'Exception:\n{ex}', config.RED)
    

if __name__ == '__main__':
    main()
