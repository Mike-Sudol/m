"""Test Dividing"""
from decimal import InvalidOperation
import pytest
from app.commands import CommandHandler
from app.plugins.divide import DivideCommand

@pytest.fixture
def command_handler():
    """Start Command Handler"""
    handler = CommandHandler()
    handler.register_command('divide', DivideCommand())
    return handler

def test_divide_command_valid(command_handler):
    """Test the "divide" command with valid inputs"""
    result = command_handler.execute_command('divide', ['6', '3'])
    assert result == 2.0

    result = command_handler.execute_command('divide', ['7.5', '2.5'])
    assert result == 3.0

def test_divide_command_zero_division(command_handler):
    """Test the "divide" command with zero division"""
    with pytest.raises(ZeroDivisionError, match="Error: Division by zero is not allowed."):
        command_handler.execute_command('divide', ['5', '0'])

def test_divide_command_invalid_args(command_handler):
    """Test the "divide" command with invalid inputs (non-numeric)"""
    with pytest.raises(ValueError, match="Error: Invalid number format. Please enter valid decimal numbers."):
        command_handler.execute_command('divide', ['10', 'abc'])

def test_divide_command_missing_args(command_handler):
    """Test the "divide" command with missing arguments"""
    with pytest.raises(ValueError, match="Two arguments are required"):
        command_handler.execute_command('divide', ['10'])
