"""Command Class and its handler"""
from abc import ABC, abstractmethod

class Command(ABC):
    """Base Command Class"""
    @abstractmethod
    def execute(self,args):
        """Command Execution"""

class CommandHandler:
    """ Command Handler Class"""
    def __init__(self):
        """Initialize CommandHandler"""
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        """Register a command"""
        self.commands[command_name] = command

    def execute_command(self, command_name: str, args):
        """Execute a command"""
        try:
            return self.commands[command_name].execute(args)
        except KeyError:
            print(f"No such command: {command_name}")
            return None
    