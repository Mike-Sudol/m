""" Manages the history of the commands sent to the CLI"""
import logging
import os
import pandas as pd

class HistoryManager:
    """Manages History for the CLI"""
    file_name = 'history.csv'
    _directory = ''
    _history = pd.DataFrame(columns=['Operation', 'Num1', 'Num2', 'Result'])

    @staticmethod
    def set_directory(directory_path):
        """Set the directory where the history file will be saved"""
        if os.path.exists(directory_path):
            HistoryManager._directory = directory_path
            logging.info(f"History file directory set to: {directory_path}")
        else:
            raise FileNotFoundError(f"The directory {directory_path} does not exist.")

    @staticmethod
    def get_file_path():
        """Get the full file path for the history file"""
        return os.path.join(HistoryManager._directory, HistoryManager.file_name)

    @staticmethod
    def add_record(operation, num1, num2, result):
        """Add a record to the history"""
        new_record = pd.DataFrame({
            'Operation': [operation],
            'Num1': [num1],
            'Num2': [num2],
            'Result': [result]
        })
        HistoryManager._history = pd.concat([HistoryManager._history, new_record], ignore_index=True)
        logging.info(f"Record added to history: {new_record.iloc[0].to_dict()}")

    @staticmethod
    def load_history():
        """Load history from the CSV file if it exists"""
        file_path = HistoryManager.get_file_path()
        if os.path.exists(file_path):
            HistoryManager._history = pd.read_csv(file_path)
            print("History loaded successfully.")
            logging.info("History Loaded successfully")
            print(HistoryManager._history)
        else:
            print("No history found.")
            logging.info("No history found")
            HistoryManager._history = pd.DataFrame(columns=['Operation', 'Num1', 'Num2', 'Result'])

    @staticmethod
    def clear_history():
        """Clear the in-memory history and delete the file"""
        file_path = HistoryManager.get_file_path()
        HistoryManager._history = pd.DataFrame(columns=['Operation', 'Num1', 'Num2', 'Result'])
        if os.path.exists(file_path):
            os.remove(file_path)
            print("History cleared.")
            logging.info("History cleared successfully")
        else:
            print("No history to clear.")
            logging.info("No history to clear")

    @staticmethod
    def delete_record(index):
        """Delete a record at the specified index"""
        try:
            index = int(index)
            if 0 <= index < len(HistoryManager._history):
                HistoryManager._history = HistoryManager._history.drop(HistoryManager._history.index[index])
                print(f"Record at position {index} deleted.")
                logging.info(f"Record at position {index} deleted.")
            else:
                print(f"Record at position {index} not found. Valid positions are 0 to {len(HistoryManager._history)-1}.")
                logging.warning(f"Record at position {index} not found. Valid positions are 0 to {len(HistoryManager._history)-1}.")
        except KeyError as e:
            print(f"Error deleting record: {e}")
            logging.error(f"Error deleting record: {e}")

    @staticmethod
    def save_history():
        """Save the in-memory history to CSV"""
        file_path = HistoryManager.get_file_path()
        try:
            HistoryManager._history.to_csv(file_path, index=False)
            print("Saved Successfully")
            logging.info("History saved successfully")
        except OSError as e:
            print(f"Error while trying to save history: {e}")
            logging.error(f"Error while trying to save history: {e}")

    @staticmethod
    def display_history():
        """Display the current in-memory history"""
        if HistoryManager._history.empty:
            print("No records in history.")
            logging.info("No records in history")
        else:
            print(HistoryManager._history)
            logging.info("History displayed")
