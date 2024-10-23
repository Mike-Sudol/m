"""Delete Command for deleting a record"""
import logging
from app.commands import Command
from app.history import HistoryManager

class DeleteCommand(Command):
    """Delete Class"""
    def __init__(self):
        """Initialize DeleteCommand.""" 

    def execute(self, args):
        """ Execute Delete """
        logging.info(f"Trying to delete record at position: '{args[0]}' ") 
        HistoryManager.delete_record(args[0])
