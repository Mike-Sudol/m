"""Clear Command for clearing calculations history"""
import logging
from app.commands import Command
from app.history import HistoryManager

class ClearCommand(Command):
    """Clear Class"""
    def __init__(self):
        """Initialize LoadCommand.""" 

    def execute(self, args):
        """ Execute Clear """
        logging.info("Trying to clear history") 
        HistoryManager.clear_history()
