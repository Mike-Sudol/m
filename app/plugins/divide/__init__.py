""" Division Command Class """
from decimal import Decimal, InvalidOperation
import logging
from app.commands import Command

class DivideCommand(Command):
    ''' Command for Division'''

    def execute(self, args):
        ''' Divide 2 Numbers and return the result '''
        if len(args) != 2:
            raise ValueError("Two arguments are required")

        try:
            number1 = Decimal(args[0])
            number2 = Decimal(args[1])
        except InvalidOperation as exc:
            raise ValueError("Error: Invalid number format. Please enter valid decimal numbers.") from exc

        if number2 == 0:
            raise ZeroDivisionError("Error: Division by zero is not allowed.")
        
        logging.info("Dividing %s / %s",number1,number2)
        result = number1 / number2
        print(f"The result of {number1} / {number2} is: {result}")
        return result
