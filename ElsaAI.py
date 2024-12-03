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

import functions


is_downloaded = False

def start_bot(start=True):
    client = TelegramClient(
        config.SESSION_NAME, 
        config.API_ID, 
        config.API_HASH
    )
    if start:
        client.start(bot_token=config.PrincessElsaAIBot_BOT_TOKEN)

    return client

def main():
    try:
        # if not session created
        if not (f'{config.SESSION_NAME}.session' in os.listdir(f'{config.THIS_SCRIPT_DIR}')):
            cmd_message_colorized(
                CMDColorLogger(), 
                f'No {config.SESSION_NAME}.session in {os.listdir({config.THIS_SCRIPT_DIR})}. Session created...',
                config.RED
            )
            bot_client = start_bot()

            cmd_message_colorized(CMDColorLogger(), f'Bot started', config.RED)
        
        # if there is a session file,
        # according to https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.auth.AuthMethods.sign_in
        # "The session file contains enough information for you to login without re-sending the code"
        if (f'{config.SESSION_NAME}.session' in os.listdir(f'{config.THIS_SCRIPT_DIR}')):
            cmd_message_colorized(CMDColorLogger(), f'Bot started', config.YELLOW)
            bot_client = start_bot(start=False)

            # Handler for the /start command
            @bot_client.on(events.NewMessage(pattern='/start'))
            async def respond_start(event):
                user = await event.get_sender()
                
                await event.respond(
                    f'Hello, {user.first_name}!\nThis bot will send you a chosen song' \
                    '(mp3 file) from a list of musician songs' \
                    ' on muzofond.fm', 
                    buttons=[ 
                        Button.inline('Choose a music artist name...')
                    ]
                )
            
            @bot_client.on(events.CallbackQuery(data=b'Choose a music artist name...'))
            async def handler(event):
                await event.respond(f'Input a name of musician. After that the bot will send the list of tracks of the chosen musician...' )

            # ------------------------------------------------------------------------------------------------------
            @bot_client.on(events.NewMessage(incoming=True))
            async def handler(event):
                event.text = event.text.strip()

                # not /start
                if ('/' not in event.text) and ('start' not in event.text):
                    artist = str(event.text).title()

                    if not any(x.isalpha() for x in artist):
                        await event.respond('Your musician\'s name didn\'t have any letters! Is it a joke? Try again with a real name...')

                    else:
                        cmd_message_colorized(CMDColorLogger(), f'You chose: {artist}', config.YELLOW)
                        
                        mfs = MuzofondMusicSaver(artist)
                        songs = mfs.get_mp3s_of_author_found_songs()
                        
                        for song in songs:
                            mp3_title = song.split(":::")[1]
                            mp3_link = song.split(":::")[0]

                            await event.respond(
                                f'{artist}, [link]({mp3_link})',
                                buttons=[
                                    Button.inline(
                                        # https://docs.telethon.dev/en/stable/modules/custom.html#telethon.tl.custom.button.Button.inline
                                        # static inline(text, data=None)
                                        # If data is omitted, the given text will be used as data
                                        f'{artist}: {mp3_title}',
                                        data=b'mp3'
                                    )
                                ]
                            )

            @bot_client.on(events.CallbackQuery(data=b'mp3'))
            async def handler(event):
                msg = await event.get_message()
                chat = await event.get_input_chat() # bot chat
                user = await event.get_sender()
                
                try:
                    song_title = str(msg.reply_markup.rows[0].buttons[0].text).split(': ')[1] # f'{artist}: {mp3_title}',
                    artist = str(msg.reply_markup.rows[0].buttons[0].text).split(': ')[0] # f'{artist}: {mp3_title}',
                    song_url = str(msg.entities[0].url)

                    # download a song 
                    try:
                        filename = f'{artist} - {song_title}'
                        await event.respond(f'{user.first_name}, please wait a little...\n {filename} is being downloaded...')

                        cmd_message_colorized(CMDColorLogger(), f'Trying to download: {filename}.mp3...', config.LIGHT_GREEN)
                        
                        is_downloaded = functions.download_file(song_url, f'{config.THIS_SCRIPT_DIR}/sent_songs/{filename}.mp3')
                        
                        if is_downloaded:
                            mfs = MuzofondMusicSaver(artist)
                            mfs.clear_mp3_metadata(f'{config.THIS_SCRIPT_DIR}/sent_songs/{filename}.mp3')

                            cmd_message_colorized(CMDColorLogger(), f'The tags are deleted from {filename}.mp3...', config.LIGHT_GREEN)
                            
                            # SENDING THE CHOSEN FILE CLEARD FROM METADATA
                            # TO THE USER
                            await bot_client.send_message(
                                chat, 
                                f'Hey, {user.first_name}!\nHere\'s your song: {filename}'
                            )
                            await event.respond(f'{user.first_name}, please wait a little... It\'s being processed')
                            await asyncio.sleep(4)
                            await event.respond(f'{user.first_name}, please wait a little... It\'s being processed')

                            # sending file
                            file = await bot_client.upload_file(f'{config.THIS_SCRIPT_DIR}/sent_songs/{filename}.mp3')
                            await bot_client.send_file(chat, file)
                            cmd_message_colorized(
                                CMDColorLogger(), 
                                f'The song {filename}.mp3 is sent.',
                                config.LIGHT_GREEN
                            )
                      
                    except Exception as ex:
                        cmd_message_colorized(CMDColorLogger(), f'Exception: download_file or clear_mp3_metadata: {ex}',config.RED)

                except Exception as ex:
                    cmd_message_colorized(CMDColorLogger(), f'Exception @bot_client.on(events.CallbackQuery(data=b\'mp3\')): {ex}', config.RED)
                
            with bot_client:
                bot_client.run_until_disconnected()

    except Exception as ex:
        cmd_message_colorized(CMDColorLogger(), f'Exception: {ex}', config.RED)

        

if __name__ == '__main__':
    main()
