"""Load Command for displaying past calculations"""
import logging
from app.commands import Command
from app.history import HistoryManager

class LoadCommand(Command):
    """Load Class"""
    def __init__(self):
        """Initialize LoadCommand.""" 

    def execute(self, args):
        """ Execute Load """
        logging.info("Trying to display history") 
        HistoryManager.display_history() 
