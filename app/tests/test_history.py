import pytest
import os
import pandas as pd
from unittest.mock import patch
from app.history import HistoryManager  # Replace with the actual module name

# Helper function to create a temporary directory for testing
@pytest.fixture
def temp_dir(tmpdir):
    return str(tmpdir)

# Test setting the directory
def test_set_directory_valid(temp_dir):
    HistoryManager.set_directory(temp_dir)
    assert HistoryManager._directory == temp_dir

def test_set_directory_invalid():
    with pytest.raises(FileNotFoundError):
        HistoryManager.set_directory("non_existent_directory")

# Test adding a record to history
def test_add_record():
    HistoryManager._history = pd.DataFrame(columns=['Operation', 'Num1', 'Num2', 'Result'])  # Reset history
    HistoryManager.add_record('add', 1, 2, 3)
    assert not HistoryManager._history.empty
    assert HistoryManager._history.iloc[0].to_dict() == {'Operation': 'add', 'Num1': 1, 'Num2': 2, 'Result': 3}

# Test loading history when file exists
@patch('pandas.read_csv')
@patch('os.path.exists', return_value=True)
def test_load_history(mock_exists, mock_read_csv):
    mock_read_csv.return_value = pd.DataFrame({
        'Operation': ['add'],
        'Num1': [1],
        'Num2': [2],
        'Result': [3]
    })
    HistoryManager.load_history()
    assert not HistoryManager._history.empty
    assert HistoryManager._history.iloc[0].to_dict() == {'Operation': 'add', 'Num1': 1, 'Num2': 2, 'Result': 3}

# Test loading history when file does not exist
@patch('os.path.exists', return_value=False)
def test_load_history_no_file(mock_exists):
    HistoryManager.load_history()
    assert HistoryManager._history.empty

# Test saving history
@patch('pandas.DataFrame.to_csv')
def test_save_history(mock_to_csv, temp_dir):
    HistoryManager.set_directory(temp_dir)
    HistoryManager.add_record('add', 1, 2, 3)
    HistoryManager.save_history()
    file_path = os.path.join(temp_dir, HistoryManager.file_name)
    mock_to_csv.assert_called_once_with(file_path, index=False)

# Test clearing history when file exists
@patch('os.path.exists', return_value=True)
@patch('os.remove')
def test_clear_history(mock_remove, mock_exists, temp_dir):
    HistoryManager.set_directory(temp_dir)
    HistoryManager.add_record('add', 1, 2, 3)
    HistoryManager.clear_history()
    assert HistoryManager._history.empty
    mock_remove.assert_called_once_with(HistoryManager.get_file_path())

# Test deleting a record
def test_delete_record():
    HistoryManager._history = pd.DataFrame({
        'Operation': ['add', 'subtract'],
        'Num1': [1, 2],
        'Num2': [2, 3],
        'Result': [3, -1]
    })
    HistoryManager.delete_record(1)
    assert len(HistoryManager._history) == 1
    assert HistoryManager._history.iloc[0].to_dict() == {'Operation': 'add', 'Num1': 1, 'Num2': 2, 'Result': 3}

# Test display history when empty
def test_display_history_empty(capsys):
    HistoryManager._history = pd.DataFrame(columns=['Operation', 'Num1', 'Num2', 'Result'])  # Reset history
    HistoryManager.display_history()
    captured = capsys.readouterr()
    assert "No records in history." in captured.out

# Test display history when not empty
def test_display_history_non_empty(capsys):
    HistoryManager._history = pd.DataFrame({
        'Operation': ['add'],
        'Num1': [1],
        'Num2': [2],
        'Result': [3]
    })
    HistoryManager.display_history()
    captured = capsys.readouterr()
    assert "add" in captured.out
