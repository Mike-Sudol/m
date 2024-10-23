"""Tests Command and CommandHandler """

from unittest.mock import patch
import pytest
from app.commands import Command, CommandHandler

class TestCommand(Command):
    """ Test Dummy Command """
    def execute(self,args):
        print("Executing TestCommand")

def test_register_command():
    """Test Register"""
    command_handler = CommandHandler()
    test_command = TestCommand()

    command_handler.register_command("test", test_command)
    assert "test" in command_handler.commands
    assert command_handler.commands["test"] == test_command

def test_execute_command():
    """Test Execute"""
    command_handler = CommandHandler()
    mock_command = TestCommand()

    with patch.object(TestCommand, 'execute') as mock_execute:
        command_handler.register_command("mock", mock_command)
        command_handler.execute_command("mock", [])
        mock_execute.assert_called_once()

def test_execute_null_command(capsys):
    """Test null command"""
    command_handler = CommandHandler()
    command_handler.execute_command("null", [])

    captured = capsys.readouterr()
    assert "No such command: null" in captured.out
