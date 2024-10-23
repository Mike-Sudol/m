"""Test Multiplying"""
from decimal import InvalidOperation
import pytest
from app.commands import CommandHandler
from app.plugins.multiply import MultiplyCommand

@pytest.fixture
def command_handler():
    """Start Command Handler"""
    handler = CommandHandler()
    handler.register_command('multiply', MultiplyCommand())
    return handler

def test_multiply_command_valid(command_handler):
    """Test the "multiply" command with valid inputs"""
    result = command_handler.execute_command('multiply', ['5', '3'])
    assert result == 15.0

    result = command_handler.execute_command('multiply', ['-1', '2.5'])
    assert result == -2.5

def test_multiply_command_invalid_args(command_handler):
    """Test the "multiply" command with invalid inputs (non-numeric)"""
    with pytest.raises(ValueError, match="Error: Invalid number format. Please enter valid decimal numbers."):
        command_handler.execute_command('multiply', ['5', 'abc'])

def test_multiply_command_missing_args(command_handler):
    """Test the "multiply" command with missing arguments"""
    with pytest.raises(ValueError, match="Two arguments are required"):
        command_handler.execute_command('multiply', ['5'])
