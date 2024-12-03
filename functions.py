import platform
from string import punctuation

from logger import CMDColorLogger, cmd_message_colorized
import config
import mutagen
from fake_headers import Headers
import wget


def get_user_os():
    return platform.system().lower()


def delete_forbidden_chars(string, out_string):
    # deleting forbidden chars
    FORBIDDEN_CHARS = re.escape(punctuation=punctuation)
    out_string = re.sub('['+FORBIDDEN_CHARS+']', '', string).replace('"', "")


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
        


url = 'https://dl3s2.muzofond.fm/aHR0cDovL2YubXAzcG9pc2submV0L21wMy8wMDMvMjM5LzA2MC8zMjM5MDYwLm1wMw=='

if __name__ == '__main__':
     clear_mp3_metadata(f'{config.THIS_SCRIPT_DIR}/sent_songs/Holly Dunn - Heart Full Of Love.mp3')
