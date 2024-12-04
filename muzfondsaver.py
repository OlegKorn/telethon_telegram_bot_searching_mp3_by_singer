from bs4 import BeautifulSoup as bs
import requests
import re, os, sys
from time import sleep
import shutil
from fake_headers import Headers
import config
from logger import CMDColorLogger, cmd_message_colorized

import mutagen

from config import THIS_SCRIPT_DIR

import functions


SEARCH_BASE_URL = 'https://muzofond.fm/search/'


class MuzofondMusicSaver(object):
    '''singleton, i.e. only 1 instance can be created'''
    def __init__(self, musician):
        self.musician = str(musician)
        self.search_url = SEARCH_BASE_URL + self.musician

    def __new__(cls, e): # without e it demands second argument
        if not hasattr(cls, 'instance'):
            cls.instance = super(MuzofondMusicSaver, cls).__new__(cls)
        return cls.instance


    def get_soup(self):
        session = requests.Session()
        
        try:
            self.request = session.get(self.search_url, headers=Headers(headers=True).generate())
            
            if self.request.status_code != 200:
                return f'Maybe the page {self.search_url} isn\'t available, status_code: {self.request.status_code}'

            self.soup = bs(self.request.content, 'html.parser')
            return self.soup
        
        except Exception as ex:
            return f'Exception: {ex}'

        except ConnectionError as ce:
            return f'ConnectionError: {ce}'

        except RequestException as re:
            return f'RequestException: {re}'

        except ConnectTimeout as ct:
            return f'ConnectionError: {ct}'

        except Timeout as t:
            return f'Timeout: {t}'


    def get_mp3s_of_author_found_songs(self):
        self.s = self.get_soup()
        mp3s_of_author = []

        try:
            page_items = self.s.find('ul', class_='mainSongs unstyled songs').find_all('li', class_='item')
        except (TypeError, AttributeError) as ex:
            print(ex)
            page_items = self.s.find('ul', class_='mainSongs unstyled songsListen songs').find_all('li', class_='item')

        try:
            for item in page_items:
                mp3_link = item.find("li", class_="play").get("data-url")
                mp3_title = item.find("span", class_="track").text.strip()
                mp3_title_cleared = functions.delete_forbidden_chars(mp3_title)

                track_data = mp3_link + ":::" + mp3_title_cleared
                mp3s_of_author.append(track_data)

            return mp3s_of_author

        except Exception as ex:
            print(f'Error: get_mp3s_of_author_page()\n, {ex}')
            return ex


    def clear_mp3_metadata(self, filepath):
        try:
            mp3 = mutagen.File(filepath)

            mp3.delete()
            mp3.save()

        except Exception as ex:
            cmd_message_colorized(
                CMDColorLogger(), 
                f'Clearing metadata:\n {ex}',
                config.RED
            )
                
            

# clear_mp3_metadata('G:/Desktop/py/TG/PrincessElsaAIBot/sent_songs/Holly Dunn - Wings on My Angel.mp3')
