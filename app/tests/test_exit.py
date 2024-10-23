""" ExitCommand Test """ 
import pytest
from app.plugins.exit import ExitCommand

def test_execute_exit():
    """ Test Exit Command"""
    exit_command = ExitCommand()
    with pytest.raises(SystemExit) as e:
        exit_command.execute([])
    assert str(e.value) == "Exiting..."
    