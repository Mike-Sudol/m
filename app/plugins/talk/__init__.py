"""Talk Command, used for testing args"""
import logging
from app.commands import Command

class TalkCommand(Command):
    """Talk Class"""
    def __init__(self):
        """Initialize TalkCommand.""" 

    def execute(self, args):
        """ Execute Talk """
        logging.info("Trying to Talk")
        print("Hello World!")
        print(args)
