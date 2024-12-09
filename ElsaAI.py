from telethon import TelegramClient, events
from telethon import errors

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
import logging, tracemalloc


is_downloaded = False

msg_ids = []


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
            cmd_message_colorized(CMDColorLogger(), 'Session created...', config.MAGENTA)
            client = start_bot()
            cmd_message_colorized(CMDColorLogger(), f'Bot started', config.MAGENTA)
        
        if (f'{config.SESSION_NAME}.session' in os.listdir(f'{config.THIS_SCRIPT_DIR}')):
            cmd_message_colorized(CMDColorLogger(), f'Bot started', config.MAGENTA)
            
            client = start_bot(start=False)
            

            try:
                @client.on(events.NewMessage(pattern='/start'))
                async def respond_start(event):
                    functions.append_msg_id(msg_ids, event.id)
                    # cmd_message_colorized(CMDColorLogger(), f'/start: {msg_ids}', config.LIGHT_GREEN)

                    if config.send_name_button_event_was_triggered and not config.send_name_button_event_was_finished:    
                        pass

                    if not config.send_name_button_event_was_triggered:
                        user = await event.get_sender() # name = utils.get_display_name(sender) ?
                        
                        msg = await event.respond(
                            f'Hello, {user.first_name} ☘️!\nThis bot will send 🎁 you a chosen song ' \
                            '(mp3 file) from a songs list of an artist you chose ' \
                            '🔊 (from muzofond.fm)', 
                            buttons=[ 
                                Button.inline('Click and send a music artist name...', b'send_name_button')
                            ]
                        )

                        functions.append_msg_id(msg_ids, msg.id)
                        # cmd_message_colorized(CMDColorLogger(), f'/start: {msg_ids}', config.LIGHT_GREEN)

            except Exception as ex:
                cmd_message_colorized(CMDColorLogger(), f'Exception: respond_start: {ex}', config.RED)
            

            try:
                @client.on(events.NewMessage(incoming=True, pattern='/delete'))
                async def delete_dialog(event):
                    functions.append_msg_id(msg_ids, event.id)
                    # cmd_message_colorized(CMDColorLogger(), f'/delete: {msg_ids}', config.LIGHT_GREEN)
                    
                    try:
                        await client.delete_messages(event.chat_id, msg_ids)
                        msg_ids.clear()
                        # cmd_message_colorized(CMDColorLogger(), f'AFTER DELETING? /delete: {msg_ids}', config.LIGHT_GREEN)
                    except Exception as ex:
                        cmd_message_colorized(CMDColorLogger(), f'Exception: delete_messages: {ex}',config.RED)
                                            
            except Exception as ex:
                cmd_message_colorized(CMDColorLogger(), f'Exception: delete_messages: {ex}',config.RED)


            # not /start and not /delete
            try:
                @client.on(events.NewMessage(pattern=r'^((?!\/start|\/delete).)*$'))
                async def respond_else(event):
                    functions.append_msg_id(msg_ids, event.id)
                    # cmd_message_colorized(CMDColorLogger(), f'/start|/delete: {msg_ids}', config.LIGHT_GREEN)

                    if config.send_name_button_event_was_triggered and not config.send_name_button_event_was_finished:
                        pass
                    
                    if not config.send_name_button_event_was_triggered:
                        # append id ot the message of "pattern=r'^((?!\/start|\/delete).)*$'" itself
                        msg = await event.respond('Try [/start](/start)...')                       
                        
                        functions.append_msg_id(msg_ids, msg.id)
                        # cmd_message_colorized(CMDColorLogger(), f'/start|/delete): {msg_ids}', config.LIGHT_GREEN)
                        
            except Exception as ex:
                cmd_message_colorized(CMDColorLogger(), f'Exception: respond_else: {ex}', config.RED)

            
            ##############################################################################
            # button
            ##############################################################################
            @client.on(events.CallbackQuery(data=b'send_name_button'))
            async def handler_send_name_button(event):
                # cmd_message_colorized(CMDColorLogger(), f'send_name_button: {msg_ids}', config.LIGHT_GREEN)

                config.send_name_button_event_was_triggered = True
                    
                msg = await event.respond(f'Type the name of a musician. After that the bot will' \
                                          ' send the list of tracks of the chosen musician...' )

                functions.append_msg_id(msg_ids, msg.id)
                # cmd_message_colorized(CMDColorLogger(), f'send_name_button: {msg_ids}', config.LIGHT_GREEN)
               
                @client.on(events.NewMessage)
                async def handler_a_name_is_chosen_after_clicking_send_name_button(event):
                    functions.append_msg_id(msg_ids, event.id)
                    # cmd_message_colorized(CMDColorLogger(), f'handler_a_name_is_chosen_after_clicking_send_name_button: {msg_ids}', config.LIGHT_GREEN)

                    try:
                        if event.text == '/delete':
                            config.send_name_button_event_was_triggered = False
                            
                        if config.send_name_button_event_was_triggered:
                            artist = str(event.text).strip().lower()
           
                            if not any(x.isalpha() for x in artist):
                                msg = await event.respond('Your musician\'s name didn\'t have any letters! Is it a joke? Try again with a real name...')
                                functions.append_msg_id(msg_ids, msg.id)
                                # cmd_message_colorized(CMDColorLogger(), f'handler_a_name_is_chosen_after_clicking_send_name_button: {msg_ids}', config.LIGHT_GREEN)

                            # elif (event.text != '/delete') and (event.text != '/start'):
                            cmd_message_colorized(CMDColorLogger(), f'You chose {artist}', config.YELLOW)
                                        
                            mfs = MuzofondMusicSaver(artist)
                            songs = mfs.get_mp3s_of_author_found_songs()
                                
                            if 'Error:' in songs[0]:
                                msg = await event.respond(f'🐖 Error: 🐖{songs[1]} 🐖.\nTry [/start](/start) or wait a little...')
                                functions.append_msg_id(msg_ids, msg.id)
                                
                                # cmd_message_colorized(
                                #     CMDColorLogger(), 
                                #     f'handler_a_name_is_chosen_after_clicking_send_name_button: {event.id} {msg.id}', 
                                #     config.RED
                                # )
                                
                            else:
                                for song in songs:
                                    mp3_title = song.split(":::")[1]
                                    mp3_link = song.split(":::")[0]

                                    msg = await event.respond(
                                        f'{artist}, [link]({mp3_link})',
                                        buttons=[
                                            Button.inline(
                                                f'🏆 {artist}: {mp3_title} 🐈',
                                                data=b'download mp3'
                                            )
                                        ]
                                    )

                                    functions.append_msg_id(msg_ids, msg.id)
                                    # cmd_message_colorized(CMDColorLogger(), f'handler_a_name_is_chosen_after_clicking_send_name_button: {msg_ids}', config.LIGHT_GREEN)

                            del mfs, songs
                    
                        # config.send_name_button_event_was_triggered = False
                        # config.send_name_button_event_was_finished = True

                    except Exception as ex:
                        cmd_message_colorized(
                            CMDColorLogger(), 
                            f'handler_a_name_is_chosen_after_clicking_send_name_button: {ex}',
                            config.RED
                        )

                    config.send_name_button_event_was_triggered = False
            
            @client.on(events.CallbackQuery(data=b'download mp3'))
            async def handler_download(event):
                button_info = await event.get_message()
                chat = await event.get_input_chat() # bot chat
                user = await event.get_sender()
                
                try:
                    song_title = str(button_info.reply_markup.rows[0].buttons[0].text).split(': ')[1] # f'{artist}: {mp3_title}',
                    artist = str(button_info.reply_markup.rows[0].buttons[0].text).split(': ')[0] # f'{artist}: {mp3_title}',
                    song_url = str(button_info.entities[0].url)

                    # download a song 
                    try:
                        filename = f'{artist} - {song_title}'
                        
                        msg = await event.respond(f'👺 {user.first_name}, 🐥 please wait a little... 🌈\n {filename} is being downloaded ⚙️ ...')
                        functions.append_msg_id(msg_ids, msg.id)

                        cmd_message_colorized(CMDColorLogger(), f'Trying to download: {filename}.mp3...', config.LIGHT_GREEN)
                        
                        is_downloaded = functions.download_file(song_url, f'{config.THIS_SCRIPT_DIR}/sent_songs/{filename}.mp3')

                        if not is_downloaded:
                            error_msg = await event.respond(f'⛔️ {user.first_name}, ⛔️ seems there is a problem downloading {filename}.')
                            error_msg2 = await event.respond('Try later 🕐🕑🕒🕓🕔🕕 or [/start](/start) or [/delete](/delete)')
                            
                            functions.append_msg_id(msg_ids, error_msg.id)
                            functions.append_msg_id(msg_ids, error_msg2.id)
                        
                        if is_downloaded:
                            mfs = MuzofondMusicSaver(artist)
                            mfs.clear_mp3_metadata(f'{config.THIS_SCRIPT_DIR}/sent_songs/{filename}.mp3')

                            cmd_message_colorized(CMDColorLogger(), f'The tags are deleted from {filename}.mp3...', config.LIGHT_GREEN)
                            
                            # SENDING THE CHOSEN FILE CLEARD FROM METADATA
                            # TO THE USER
                            msg = await event.respond(f'{user.first_name}, please wait a little... It\'s being processed 🕐')
                            functions.append_msg_id(msg_ids, msg.id)
                            await asyncio.sleep(4)
                            
                            msg = await event.respond(f'{user.first_name}, Still being processed... 🕑')
                            functions.append_msg_id(msg_ids, msg.id)
                            await asyncio.sleep(4)
                            
                            msg = await event.respond(f'{user.first_name}, Don\'t panic, if you see this message - it\'s still being processed... 🕒')
                            functions.append_msg_id(msg_ids, msg.id)
                            await asyncio.sleep(4)
                            
                            msg = await event.respond(f'{user.first_name}, Just 10-15 seconds... It\'s being processed 🕓')
                            functions.append_msg_id(msg_ids, msg.id)
                            await asyncio.sleep(4)
                            
                            msg = await event.respond(f'{user.first_name}, A little patience... It\'s STILL being processed 🕔')
                            functions.append_msg_id(msg_ids, msg.id)
                            await asyncio.sleep(4)
                            
                            msg = await event.respond(f'{user.first_name}, Yes! It\'s STILL being processed 🕕')
                            functions.append_msg_id(msg_ids, msg.id)

                            # sending file
                            file = await client.upload_file(f'{config.THIS_SCRIPT_DIR}/sent_songs/{filename}.mp3')
                            
                            msg_file = await client.send_file(chat, file)
                            functions.append_msg_id(msg_ids, msg.id)

                            msg = await client.send_message(
                                chat, 
                                f'🐥 Hey, {user.first_name}!\nHere\'s your song: {filename}'
                            )
                            functions.append_msg_id(msg_ids, msg.id)

                            cmd_message_colorized(
                                CMDColorLogger(), 
                                f'The song {filename}.mp3 is sent.',
                                config.LIGHT_GREEN
                            )
                      
                    except Exception as ex:
                        cmd_message_colorized(CMDColorLogger(), f'Exception: download_file or clear_mp3_metadata: {ex}',config.RED)
                
                except Exception as ex:
                    cmd_message_colorized(CMDColorLogger(), f'Exception @client.on(events.CallbackQuery(data=b\'mp3\')): {ex}', config.RED)

            with client:
                client.run_until_disconnected()

    except Exception as ex:
        cmd_message_colorized(CMDColorLogger(), f'Exception: {ex}', config.RED)
    except errors.FloodWaitError as ex:
        cmd_message_colorized(CMDColorLogger(), f'Have to sleep: {ex.seconds}', config.RED)
        asyncio.sleep(ex.seconds)

        

if __name__ == '__main__':
    main()
