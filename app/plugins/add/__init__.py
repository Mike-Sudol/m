""" Add Command Class"""
from decimal import Decimal, InvalidOperation
import logging
from app.commands import Command

class AddCommand(Command):
    ''' Command for Addition'''

    def execute(self, args):
        ''' Add 2 Numbers, Prints the output'''
        if len(args) != 2:
            logging.error("Two arguments are required")
            raise ValueError("Two arguments are required")
        try:
            number1 = Decimal(args[0])
            number2 = Decimal(args[1])
            logging.info("Adding %s + %s",number1,number2)

            result = number1 + number2
            print(f"The result of {number1} + {number2} is: {result}")
            return result
        except InvalidOperation as exc:
            logging.error("Error: Invalid number format. Please enter valid decimal numbers.")
            raise ValueError("Error: Invalid number format. Please enter valid decimal numbers.") from exc
