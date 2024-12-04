import platform
from string import punctuation

from logger import CMDColorLogger, cmd_message_colorized
import config
import mutagen
from fake_headers import Headers
import wget
import re 
from string import punctuation


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
            f'Clearing metadata:\n {ex}',
            config.RED
        )


def download_file(url, filename, marker=False):
    try:
        wget.download(url, filename)
        
        cmd_message_colorized(
            CMDColorLogger(), 
            f'Downloading of {filename} is finished',
            config.YELLOW
        )
        
        marker = True
        return marker

    except Exception as ex:
        cmd_message_colorized(
            CMDColorLogger(), 
            f'Clearing metadata:\n {ex}',
            config.RED
        )
