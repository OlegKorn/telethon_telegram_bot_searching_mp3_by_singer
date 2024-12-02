import sys
import argparse 
import pathlib
from termcolor import colored


class CMDColorLogger(object):
    '''trying to make a singleton
    Singleton provides you with a mechanism to have one, and only one, object of a
    given type and provides a global point of access. Hence, Singletons are typically
    used in cases such as logging or database operations
    1. We will allow the creation of only one instance of the Singleton class.
    2. If an instance exists, we will serve the same object again.'''
    def __init__(self):
        if 'colorama' not in sys.modules:
            import colorama
            colorama.init()
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CMDColorLogger, cls).__new__(cls)

        return cls.instance
    
    def log(self, message, color):
        '''Prints out in cmd colorized'''
        print(colored(message, color, attrs=['bold']))

def log_message_colorized(logger, message, color):
    logger.log(message, color)


parser = argparse.ArgumentParser()
parser.add_argument(
    '--gn',
    type=str, 
    help='tg group name'
)
parser.add_argument(
    '--u',
    type=str, 
    help='tg user',
    default='r3pt1101d'
)
parser.add_argument(
    '--msg',
    type=str, 
    help='tg message to --tgu'
)
parser.add_argument(
    '--img',
    type=pathlib.Path,
    help='path to a file'
)

args = parser.parse_args()

if args.u is None:
    parser.print_help()
