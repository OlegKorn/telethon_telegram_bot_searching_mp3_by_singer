import asyncio
from telethon import TelegramClient
from telethon.tl import functions, types
from time import sleep
import os, re, sys
from loguru import logger
import string
import random

 
# https://github.com/goq/telegram-list?tab=readme-ov-file
APP_ID = 24436001
APP_HASH = ''
TOKEN = ':'
PHONE = '+'

session_name = 'test'

tg_channel = 'jobs_abroad'
tg_channel_url = f'https://t.me/{tg_channel}'

THIS_SCRIPT_DIR = 'G:/Desktop/py/TG'


email = ['https://t.me/avvocatoterrasini1', 'kornilovoy@gmail.com']
    
pet_projects = [
    'https://github.com/s3rgeym/hh-applicant-tool',
    'https://github.com/s3rgeym/cpanel-api',
    'https://github.com/s3rgeym/massmail'
]

#email
message_part_1 = ''' 
Note: my email credentials differ from my name, it's made on purpose
---------------------
Hello, my name is Sergey, and I’m a skilled developer with over 15 years of experience in developing, optimizing, and maintaining web applications, APIs, and complex infrastructure solutions. I specialize in backend development with Python (especially using FastAPI) and frontend development using Vue.js. I know linux, bash very well, as well as database, network, websites managing and have broad experience with the needed tools. I have experience in system administration on Linux systems, project management, automation, DevOps, CI/CD, and containerization (Docker and Kubernetes). '''

message_part_2 = '''
I have my own security testing tools in Python, I'll show them on demand. These are my recently developed tools I use in daily life:'''

message_part_3 = '''
------------------------------------------
MY COMMERCIAL AND PET-PROJECTS EXPERIENCE:
------------------------------------------'''

experience = [
    '• As a freelancer, I develop(ed) and maintain(ed) VK bots, apps backend, student tasks, parsers, PHP backend, websites, backend, SPA, PHP / Python / JS legacy code',
    '• Have my own security testing solutions and tools, conduct(ed) penetration / security tests of apps, websites, network devices, operating systems, databases, deliver(ed) detailed reports of their findings',
    '• Developed end-to-end product',
    '• Used data pipeline tools such as Kafka, Spark Streaming',
    '• Used Postgres, MongoDB',
    '• Developed with testing methodologies and tools',
    '• Set up a Linux environment',
    '• Created cloud deployment using Kubernetes and Docker',
    '• Developed big data Python modules, automated operation tasks',
    '• Communicated with stakeholders to find, architect and developed needed solutions, enhanced test automation',
    '• Managed Azure infrastructure deployment and maintenance, built and optimized CI/CD pipelines, automated operational processes, analyzed data, collaborated with cross-functional teams',
    '• Backend development of webb app (Python, Django)',
    '• Built RESTful APIs in Python, with suitable unit, integration and end-to-end test coverage',
    '• Improved the development environment',
    '• Set up Docker configuration for local and testing environments',
    '• Developed API with FastAPI',
    '• Designed and implemented robust and scalable data pipelines using Snowflake, SQLAlchemy, and Python to extract, transform, and load (ETL) data from various sources'
]

end_message = '''
Please give me a feedback.'''


def create_and_log_message():
    id_ = id_generator()
    logger.info(id_)
    logger.info('\n')
    
    randomize(email)
    for i in email:
        logger.info(i)

    logger.info(message_part_1)
    logger.info(message_part_2)
    
    randomize(pet_projects)
    for i in pet_projects:
        logger.info(i)

    logger.info(message_part_3)
    randomize(experience)
    for i in experience:
        logger.info(str(i))

    logger.info(end_message)
    logger.info('***END OF THE POST*** ***END OF THE POST*** ***END OF THE POST*** ***END OF THE POST*** ***END OF THE POST***')


def randomize(lst):
    random.shuffle(lst)
    return lst


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


def log():
    logger.add(
        f"{THIS_SCRIPT_DIR}/{tg_channel}_test.log", 
        encoding="utf8",         
        format="{message}", 
        level="INFO"
    )

client = TelegramClient(session_name, APP_ID, APP_HASH)
client.start()

async def main():
    log()

    sleep(1)
    channel = await client.get_entity(tg_channel)
    sleep(1)
    messages = await client.get_messages(tg_channel, limit=None)

    for message in messages: 
        markers = [
            'Python', 'python', 'Django', 'vue.js', 
            'Vue.js', 'поддержка сайта', 'Flask', 
            'Python developer', 'Разработчик Python', 
            'maintaining infrastructure', 'configuring networks'
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

                logger.info('--------------------------------------------------------')

                logger.info('CONTACTS:')
                if email is not None:
                    logger.info(email)
                if tg_nick is not None:
                    logger.info(tg_nick)
                if tg_nick_from_link is not None:
                    logger.info(tg_nick_from_link)
                
                logger.info(message.id)
                logger.info(tg_channel_url)
                logger.info(cleared_message)
                logger.info('--------------------------------------------------------\n\n')

                create_and_log_message()
                logger.info('******************************************************\n\n\n\n\n')

            if not any(marker in message.text for marker in markers):
                print(message.id, ' ----> no markers')
        
        except Exception as e:
            print(message.id, ' ----> ', e)
            continue


sleep(1)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())


'''
email_re = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+'
s = 'Жду ваше резюме и вопросы на recruit@ibitcy.com или же в телеграм @leksdmiv. https://t.me/23242rwsdfs'
s1 = 'м @leksdmiv. h   recruit@ibitcy.com  https://t.me/ererwer3dfdfs sdfsd' 

try:
    email = re.search(email_re, s1)
    if email:
        email = email.group()
        print(email)
        
    tg_nick = re.search(r'(?<=@)[a-zA-Z]*', s1)
    if tg_nick:
        tg_nick = '@' + tg_nick.group()
        print(tg_nick)
                    
    tg_nick_from_link = re.search(r'(https://t.me/).*', s1)
    if tg_nick_from_link:
        tg_nick_from_link = '@' + tg_nick_from_link.group()
        print(tg_nick_from_link)

except AttributeError as e:
    print(e)
'''
