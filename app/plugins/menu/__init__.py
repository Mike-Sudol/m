"""Module containing command-related classes."""
import logging
from app.commands import Command

class MenuCommand(Command):
    """Class representing a menu command."""

    def __init__(self, command_handler):
        """Initialize MenuCommand."""
        super().__init__()
        self.command_handler = command_handler

    def execute(self, args):
        """Execute the menu command."""
        logging.info("Menu Opened")
        print("Available commands:")
        for command_name in self.command_handler.commands.keys():
            print("-", command_name)
        logging.info("Menu Closed")
        