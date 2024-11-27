import asyncio
from telethon import TelegramClient
from telethon.tl import functions, types
from time import sleep
import os, re, sys
import argparse
# from loguru import logging
import string
import random
import logging


APP_ID = 24436001
APP_HASH = ''
TOKEN = '7937555927:'
PHONE = '+'

session_name = 'test'

THIS_SCRIPT_DIR = 'G:/Desktop/py/TG'

text = '''
Python, Django, Vue.js, Docker, Kubernetes, linux, bash, FastAPI, all kinds of scripts.

{I'M SEARCHING FOR A REMOTE JOB, PART-TIME PROJECT, ETC. | I'M LOOKING FOR A REMOTE JOB - OR A PROJECT.}

{Hello | Good day | Hi there | Hi}, {my name is | I am | This is | It's} Sergey, {I specialize in developing and maintaining backend solutions using Python|develop frontend / backend in Python}, {experienced with backend frameworks and API integration | with comprehensive knowledge of security principles},{I’m | } a {motivated and skilled developer with problem-solving skills | skilled developer with problem-solving skills | experienced software developer with problem-solving skills | passionate and experienced developer with problem-solving skills | long-praticing software developer with problem-solving skills | Python developer with problem-solving skills | experienced Python developer | Python software developer} with {over 15 years of experience | 14+ years | more than 10 years | with more than 13 years of experience | commercial and open-source experience | huge commercial and open-source experience | good understanding of Python; as well as experienced | good knowledge of API and integrations, and huge experience} in {implementing services using open-source software and other resources | developing, optimizing, and maintaining web applications | Python, JS developing, maintaining web-applications | developing of web apps, SPA, Python, JS, administration}, {developing APIs | FastAPI | creating APIs | using FastAPI and creating APIs | developing APIs in FastAPI}. I {specialize | today usually specialize | have expertise | have experience | am experienced | work} in {backend development with Python | Python backend development | backend development | the development of backend in Python | Python and especially backend | Python3x development | Python and JS development} ({especially using FastAPI | I love FastAPI | especially in FastAPI | my preferable is FastAPI}) and {frontend development using Vue.js | frontend with Vue.js | Vue.js as frontend | Vue.js as frontend | frontend with Vue.js | Vue.js}. I {know linux, bash very well | bash and linux well | know bash / linux well | profoundly use linux / bash | am experienced with linux and bash | love linux and bash | use linux and bash on expert level | love and use bash and linux | know linux, bash | deeply knoow linux and bash}, as well as {database, network, websites managing | DB, networking ans webites administration | networking, DB and web administration | websites administration, networking tools and DBs | proficiency in access control models and network security} and {have broad experience with the needed tools | I am experienced with networking tools | have huge understanding of networking and protocols}, as well as {automation, DevOps, CI/CD, and containerization (Docker and Kubernetes) | demonstrated expertise with Kubernetes and Docker | DevOps, CI/CD, Docker/Kubernetes and proficient understanding of code versioning tools such as Git and Github | knowledge of CDNs (e.g. Cloudflare), DNS, certificates, and domain management}. 
{These are the tools | Here are my developed tools | This are my pety-projects for daily use | These are my own tools} I developed {among others | as well as others | for daily use | for myself}: github: s3rgeym/massmail, s3rgeym/cpanel-api, s3rgeym/hh-applicant-tool.  
This is {my general info | info about me in general | a short info about me | a short bio of mine | a little description of my experience | a little introduction | my little introduction | my short bio}. If {you are interested | it is interesting}, please {give me a feedback | write me back | give me an answer | answer me | write to me | drop me a line | send me a message | email me}. My email: gmail - kornilovoy'''


def randomize(s: str) -> str:
    while (
        s1 := re.sub(
            r"{([^{}]+)}",
            lambda m: random.choice(
                m.group(1).split(" | "),
            ),
            s,
        )
    ) != s:
        s = s1
    return s

def id_generator(size=16, chars=string.ascii_lowercase + string.digits):
    return  '(Anti-spam id): ' + ''.join(random.choice(chars) for _ in range(size))

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

    return emoji_pattern.sub(r'', string)


def log(tg_channel_name):
    '''
    logging.add(
        f"{THIS_SCRIPT_DIR}/{tg_channel}.log", 
        encoding="utf8",         
        format="{message}", 
        level="INFO"
    )
    '''
    FORMAT = '%(message)s'
    logging.basicConfig(
        filename=f'{THIS_SCRIPT_DIR}/{tg_channel_name}.log', 
        level=logging.INFO,
        format=FORMAT
    )
 
client = TelegramClient(session_name, APP_ID, APP_HASH)
client.start()

async def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--telegram_group_name',
        type=str,
        required=True,
        help=('TG public group'),
    )

    args = parser.parse_args()

    tg_group_url = f'https://t.me/{args.telegram_group_name}'
    log(args.telegram_group_name)

    sleep(1)
    channel = await client.get_entity(args.telegram_group_name)
    sleep(1)
    messages = await client.get_messages(args.telegram_group_name, limit=None)

    for message in messages: 
        await asyncio.sleep(0.2)
        '''
        markers = [
            'Python', 'python', 'Django', 'vue.js', 
            'Vue.js', 'поддержка сайта', 'Flask', 
            'Python developer', 'Разработчик Python', 
            'maintaining infrastructure', 'configuring networks'
        ]
        '''
        markers = [
            'Python', 'python', 'Junior', 'Python developer'
        ]
                
        try:
            if any(marker in message.text for marker in markers):
                cleared_message = str(remove_emoji(message.text))

                email_re = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+'

                email = re.search(email_re, cleared_message)
                if email is not None:
                    email = email.group()
                    print(message.id, email)
                            
                tg_nick = re.search(r'(?<=@)[a-zA-Z0-9_]*', cleared_message)
                if tg_nick is not None:
                    tg_nick = '@' + tg_nick.group()
                    print(message.id, tg_nick)
                                        
                tg_nick_from_link = re.search(r'(https://t.me/).*', cleared_message)
                if tg_nick_from_link is not None:
                    tg_nick_from_link = '@' + tg_nick_from_link.group()
                    print(message.id, tg_nick_from_link)

                logging.info('--------------------------------------------------------')

                logging.info('CONTACTS:')
                if email is not None:
                    logging.info(email)
                if tg_nick is not None:
                    logging.info(tg_nick)
                if tg_nick_from_link is not None:
                    logging.info(tg_nick_from_link)
                
                logging.info(message.id)
                logging.info(tg_group_url)
                logging.info(cleared_message)
                logging.info('--------------------------------------------------------\n')

                my_message = randomize(text)
                
                logging.info('CONTACTS:')
                if email is not None:
                    logging.info(email)
                if tg_nick is not None:
                    logging.info(tg_nick)
                if tg_nick_from_link is not None:
                    logging.info(tg_nick_from_link)

                logging.info(my_message)
                logging.info('******************************************************\n\n\n')

            if not any(marker in message.text for marker in markers):
                print(message.id, ' ----> no markers')
        
        except Exception as e:
            print(message.id, ' ----> ', e)
            continue

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

# print(randomize(text))
