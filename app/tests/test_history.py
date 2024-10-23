""" Test the HistoryManager """
import os
from unittest.mock import patch
import pytest
import pandas as pd
from app.history import HistoryManager

@pytest.fixture
def temp_dir(tmpdir):
    """Temp Directory for Testing"""
    return str(tmpdir)

def test_set_directory_valid(temp_dir):
    """Test if gets right directory"""
    HistoryManager.set_directory(temp_dir)
    assert HistoryManager._directory == temp_dir

def test_set_directory_invalid():
    """Check if exception gets raised"""
    with pytest.raises(FileNotFoundError):
        HistoryManager.set_directory("non_existent_directory")

def test_add_record():
    """Tests adding a record"""
    HistoryManager._history = pd.DataFrame(columns=['Operation', 'Num1', 'Num2', 'Result'])  # Reset history
    HistoryManager.add_record('add', 1, 2, 3)
    assert not HistoryManager._history.empty
    assert HistoryManager._history.iloc[0].to_dict() == {'Operation': 'add', 'Num1': 1, 'Num2': 2, 'Result': 3}

@patch('pandas.read_csv')
@patch('os.path.exists', return_value=True)
def test_load_history(mock_exists, mock_read_csv):
    """Tests loading the history"""
    mock_read_csv.return_value = pd.DataFrame({
        'Operation': ['add'],
        'Num1': [1],
        'Num2': [2],
        'Result': [3]
    })
    HistoryManager.load_history()
    assert not HistoryManager._history.empty
    assert HistoryManager._history.iloc[0].to_dict() == {'Operation': 'add', 'Num1': 1, 'Num2': 2, 'Result': 3}

@patch('os.path.exists', return_value=False)
def test_load_history_no_file(mock_exists):
    """Tests if history empty"""
    HistoryManager.load_history()
    assert HistoryManager._history.empty

@patch('pandas.DataFrame.to_csv')
def test_save_history(mock_to_csv, temp_dir):
    """Tests Saving"""
    HistoryManager.set_directory(temp_dir)
    HistoryManager.add_record('add', 1, 2, 3)
    HistoryManager.save_history()
    file_path = os.path.join(temp_dir, HistoryManager.file_name)
    mock_to_csv.assert_called_once_with(file_path, index=False)

@patch('os.path.exists', return_value=True)
@patch('os.remove')
def test_clear_history(mock_remove, mock_exists, temp_dir):
    """Tests Clearing history"""
    HistoryManager.set_directory(temp_dir)
    HistoryManager.add_record('add', 1, 2, 3)
    HistoryManager.clear_history()
    assert HistoryManager._history.empty
    mock_remove.assert_called_once_with(HistoryManager.get_file_path())

def test_delete_record():
    """Tests Deleting Record"""
    HistoryManager._history = pd.DataFrame({
        'Operation': ['add', 'subtract'],
        'Num1': [1, 2],
        'Num2': [2, 3],
        'Result': [3, -1]
    })
    HistoryManager.delete_record(1)
    assert len(HistoryManager._history) == 1
    assert HistoryManager._history.iloc[0].to_dict() == {'Operation': 'add', 'Num1': 1, 'Num2': 2, 'Result': 3}

def test_display_history_empty(capsys):
    """Tests Displaying History Empty"""
    HistoryManager._history = pd.DataFrame(columns=['Operation', 'Num1', 'Num2', 'Result'])
    HistoryManager.display_history()
    captured = capsys.readouterr()
    assert "No records in history." in captured.out

def test_display_history_non_empty(capsys):
    """Tests Displaying History when Non-Empty"""
    HistoryManager._history = pd.DataFrame({
        'Operation': ['add'],
        'Num1': [1],
        'Num2': [2],
        'Result': [3]
    })
    HistoryManager.display_history()
    captured = capsys.readouterr()
    assert "add" in captured.out
