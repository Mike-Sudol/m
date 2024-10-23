"""Display Command for displaying past calculations"""
import logging
from app.commands import Command
from app.history import HistoryManager

class DisplayCommand(Command):
    """Display Class"""
    def __init__(self):
        """Initialize DisplayCommand.""" 

    def execute(self, args):
        """ Execute Display """
        logging.info("Trying to display history")
        HistoryManager.display_history()
