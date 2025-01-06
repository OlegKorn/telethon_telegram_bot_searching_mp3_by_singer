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

from multiprocessing import Pool


class MuzofondMusicSaver(object):
    '''singleton, i.e. only 1 instance can be created'''
    def __init__(self, musician):
        self.musician = musician
        self.search_url = f'https://muzofond.fm/collections/artists/{musician}'

    def __new__(cls, e): # without e it demands second argument
        if not hasattr(cls, 'instance'):
            cls.instance = super(MuzofondMusicSaver, cls).__new__(cls)
        return cls.instance


    @functions.timeit
    def get_soup(self):
        session = requests.Session()
        
        try:
            self.request = session.get(self.search_url, headers=Headers(headers=True).generate())
            
            if self.request.status_code != 200:
                return False
            
            self.soup = bs(self.request.content, 'html.parser')
            return self.soup
        
        except Exception as ex:
            return False


    @functions.timeit
    def get_mp3s_of_author_found_songs(self):
        mp3s_of_author = []

        self.s = self.get_soup()

        if not self.s:
            return f'Error: no such author on muzofond.fm - {self.musician}'
        
        try:
            page_items = self.s.find('ul', attrs ={"data-url": f"{self.search_url}"}).find_all('li', class_='item')
            
            for item in page_items:
                mp3_link = item.find("li", class_="play").get("data-url")
                mp3_title = item.find("span", class_="track").text.strip()        
                mp3_title_cleared = functions.delete_forbidden_chars(mp3_title)

                track_data = mp3_link + ":::" + mp3_title_cleared
                mp3s_of_author.append(track_data)

            return mp3s_of_author

        except (Exception, TypeError, AttributeError) as ex:
            return 'Error: except (Exception, TypeError, AttributeError) as ex: - no such author'


    @functions.timeit
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
