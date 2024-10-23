"""Test Subtracting"""
from decimal import InvalidOperation
import pytest
from app.commands import CommandHandler
from app.plugins.subtract import SubtractionCommand

@pytest.fixture
def command_handler():
    """Start Command Handler"""
    handler = CommandHandler()
    handler.register_command('subtract', SubtractionCommand())
    return handler

def test_subtract_command_valid(command_handler):
    """Test the "subtract" command with valid inputs"""
    result = command_handler.execute_command('subtract', ['5', '3'])
    assert result == 2.0

    result = command_handler.execute_command('subtract', ['-1', '2.5'])
    assert result == -3.5

def test_subtract_command_invalid_args(command_handler):
    """Test the "subtract" command with invalid inputs (non-numeric)"""
    with pytest.raises(ValueError, match="Error: Invalid number format. Please enter valid decimal numbers."):
        command_handler.execute_command('subtract', ['5', 'abc'])

def test_subtract_command_missing_args(command_handler):
    """Test the "subtract" command with missing arguments"""
    with pytest.raises(ValueError, match="Two arguments are required"):
        command_handler.execute_command('subtract', ['5'])
