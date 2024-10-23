"""Save Command for saving history"""
import logging
from app.commands import Command
from app.history import HistoryManager

class SaveCommand(Command):
    """Save Class"""
    def __init__(self):
        """Initialize SaveCommand.""" 

    def execute(self, args):
        """ Execute Save """
        logging.info("Trying to save history") 
        HistoryManager.save_history()
