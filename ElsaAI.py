from telethon import TelegramClient, events
from telethon.tl.custom import Button

import logger
from logger import CMDColorLogger, log_message_colorized

import asyncio
import os, re, sys
import config 


def main():
    bot_client = TelegramClient(
        config.SESSION_NAME, 
        config.API_ID, 
        config.API_HASH
    )
    bot_client.start(bot_token=config.PrincessElsaAIBot_BOT_TOKEN)

    try:
        async def get_event_chat(e):
            chat = await e.get_chat()
            
            return chat

        # Handler for the /start command
        @bot_client.on(events.NewMessage(pattern='/start'))
        async def respond_start(event):
            '''
            me =
                id=8156286949,
                is_self=True,
                contact=False,
                mutual_contact=False,
                deleted=False,
                bot=True,
                bot_chat_history=False,
                bot_nochats=False,
                verified=False,
                restricted=False,
                min=False,
                bot_inline_geo=False,
                support=False,
                scam=False,
                apply_min_photo=True,
                fake=False,
                bot_attach_menu=False,
                premium=False,
                attach_menu_enabled=False,
                bot_can_edit=True,
                close_friend=False,
                stories_hidden=False,
                stories_unavailable=True,
                contact_require_premium=False,
                bot_business=False,
                bot_has_main_app=False,
                access_hash=948385373127645805,
                first_name='PrincessElsaAIBot',
                last_name=None,
                username='PrincessElsaAIbot',
                phone=None,
                photo=None,
                status=None,
                bot_info_version=1,
                restriction_reason=[
            ],
                bot_inline_placeholder=None,
                lang_code=None,
                emoji_status=None,
                usernames=[],
                stories_max_id=None,
                color=None,
                profile_color=None,
                bot_active_users=None
            '''
            me = await bot_client.get_me()
            await event.respond(
                f'Hello, {me.first_name}! I am a Telethon bot. How can I assist you today?', 
                buttons=[
                    Button.inline('respond_start!'), 
                    Button.inline('respond_start')
                ]
            )

        @bot_client.on(events.NewMessage(pattern='/new'))
        async def respond_new(event):
            me = await bot_client.get_me()
            
            await event.respond(
                f'Hey, {me.first_name}!', 
                buttons=[
                    Button.inline('respond_new'),
                    Button.inline('respond_new')
                ]
            )

    except Exception as ex:
        print(ex)
    
    with bot_client:
        bot_client.run_until_disconnected()

if __name__ == '__main__':
    main()
