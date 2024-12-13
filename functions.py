import platform
from string import punctuation

from logger import CMDColorLogger, cmd_message_colorized
import config
import mutagen
from fake_headers import Headers
import wget
import re 
from string import punctuation

import requests
import time
import functools
import typing

import inspect

import tempfile 


def timeit(fn: typing.Callable) -> typing.Callable:
    @functools.wraps(fn)
    def timed(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        try:
            dt = -time.monotonic()
            return fn(*args, **kwargs)
        finally:
            dt += time.monotonic()
            
            cmd_message_colorized(
                CMDColorLogger(), 
                f'Function "{fn.__name__}()" took {dt:.3f} seconds',
                config.MAGENTA
            )

    return timed


def get_user_os():
    return platform.system().lower()


def delete_forbidden_chars(string):
    # deleting forbidden chars
    FORBIDDEN_CHARS = re.escape(punctuation)
    cleared_string = re.sub('['+FORBIDDEN_CHARS+']', '', string).replace('"', "")
    
    return cleared_string


def clear_mp3_metadata(filepath):
    try:
        mp3 = mutagen.File(filepath)

        mp3.delete()
        mp3.save()

        cmd_message_colorized(
            CMDColorLogger(), 
            'Finished',
            config.YELLOW
        )

    except Exception as ex:
        cmd_message_colorized(
            CMDColorLogger(), 
            f'Clearing metadata: {ex}',
            config.RED
        )


@timeit
def download_file(url, filename, bar=wget.bar_thermometer, marker=False):
    try:
        wget.download(url, filename)
        
        cmd_message_colorized(
            CMDColorLogger(), 
            f'\nDownloading of {filename} is finished',
            config.YELLOW
        )
        
        marker = True
        return marker

    except Exception as ex:
        cmd_message_colorized(
            CMDColorLogger(), 
            f'download_file(): {ex}',
            config.RED
        )

        marker = False
        return [marker, ex]
        

@timeit
def return_chosen_mp3_requested_content(url):
    chosen_mp3_requested_content = requests.get(url).content
    return chosen_mp3_requested_content


def append_msg_id(lst, id_):
    if id_ not in lst:
        lst.append(id_)
    pass
