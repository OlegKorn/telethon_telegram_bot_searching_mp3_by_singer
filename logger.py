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

def cmd_message_colorized(logger, message, color):
    logger.log(message, color)
