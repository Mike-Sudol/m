""" Exit Command Class """
import sys
import logging
from app.commands import Command


class ExitCommand(Command):
    """ Exit Command"""
    def execute(self, args):
        logging.info("Preparing to Exit")
        raise SystemExit("Exiting...")
    