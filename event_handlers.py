
# Handler for the /start command
@bot_client.on(events.NewMessage(pattern='/start'))
async def respond_start(event):
    me = await bot_client.get_me() 
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

    await event.respond(f'Hello, {me.first_name}! I am a Telethon bot. How can I assist you today?')
