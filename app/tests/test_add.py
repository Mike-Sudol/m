"""Test Adding"""
from decimal import InvalidOperation
import pytest
from app.commands import CommandHandler
from app.plugins.add import AddCommand

@pytest.fixture
def command_handler():
    """Start Command Handler"""
    handler = CommandHandler()
    handler.register_command('add', AddCommand())
    return handler

def test_add_command_valid(command_handler):
    '''Test the "add" command with valid inputs'''
    result = command_handler.execute_command('add', ['5', '3'])
    assert result == 8.0

    result = command_handler.execute_command('add', ['-1', '2.5'])
    assert result == 1.5

def test_add_command_invalid_args(command_handler):
    """Test the "add" command with invalid inputs (non-numeric)"""
    with pytest.raises(ValueError, match="Error: Invalid number format. Please enter valid decimal numbers."):
        command_handler.execute_command('add', ['5', 'abc'])

def test_add_command_missing_args(command_handler):
    """Test the "add" command with missing arguments"""
    with pytest.raises(ValueError, match="Two arguments are required"):
        command_handler.execute_command('add', ['5'])
        