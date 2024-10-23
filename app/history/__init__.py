""" Manages the history of the commands sent to the CLI"""
import logging
import pandas as pd
import os

class HistoryManager:
    file_name = 'history.csv'
    _history = pd.DataFrame(columns=['Operation', 'Num1', 'Num2', 'Result'])

    @staticmethod
    def add_record(operation, num1, num2, result):
        """Add a record to the history"""
        new_record = {'Operation': operation, 'Num1': num1, 'Num2': num2, 'Result': result}
        HistoryManager._history = HistoryManager._history._append(new_record, ignore_index=True)
        logging.info(f"Record added to history'{new_record}")

    @staticmethod
    def load_history():
        """Load history from the CSV file if it exists"""
        if os.path.exists(HistoryManager.file_name):
            HistoryManager._history = pd.read_csv(HistoryManager.file_name)
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
        HistoryManager._history = pd.DataFrame(columns=['Operation', 'Num1', 'Num2', 'Result'])
        if os.path.exists(HistoryManager.file_name):
            os.remove(HistoryManager.file_name)
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
        except Exception as e:
            print(f"Error deleting record: {e}")
            logging.error(f"Error deleting record: {e}")

    @staticmethod
    def save_history():
        """Save the in-memory history to CSV"""
        try:
            HistoryManager._history.to_csv(HistoryManager.file_name, index=False)
            print("Saved Successfully")
            logging.info("History saved successfully")
        except Exception as e:
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