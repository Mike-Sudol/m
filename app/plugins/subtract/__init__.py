""" Subtraction Command Class"""
from decimal import Decimal, InvalidOperation
import logging
from app.commands import Command

class SubtractionCommand(Command):
    ''' Command for Subtraction'''

    def execute(self, args):
        ''' Subtract 2 Numbers, Returns the result'''
        if len(args) != 2:
            logging.error("Two arguments are required")
            raise ValueError("Two arguments are required")
        try:
            number1 = Decimal(args[0])
            number2 = Decimal(args[1])
            logging.info("Subtracting %s - %s",number1,number2)
            result = number1 - number2
            print(f"The result of {number1} - {number2} is: {result}")
            return result
        except InvalidOperation as exc:
            logging.error("Error: Invalid number format. Please enter valid decimal numbers.")
            raise ValueError("Error: Invalid number format. Please enter valid decimal numbers.") from exc
        