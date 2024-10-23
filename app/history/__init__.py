""" Manages the history of the commands sent to the CLI"""
import pandas as pd
import os

class HistoryManager:
    file_name = 'history.csv'

    @staticmethod
    def add_record(operation, num1, num2, result):
        # Load existing history if the file exists, otherwise create an empty dataframe
        if os.path.exists(HistoryManager.file_name):
            history = pd.read_csv(HistoryManager.file_name)
        else:
            history = pd.DataFrame(columns=['Operation', 'Num1', 'Num2', 'Result'])
        
        # Add a new record with operation and numbers
        new_record = {'Operation': operation, 'Num1': num1, 'Num2': num2, 'Result': result}
        history = history._append(new_record, ignore_index=True)
        
        # Save the updated history
        history.to_csv(HistoryManager.file_name, index=False)

    @staticmethod
    def load_history():
        # Load history from the CSV file if it exists
        if os.path.exists(HistoryManager.file_name):
            history = pd.read_csv(HistoryManager.file_name)
            print("History loaded successfully.")
            print(history)
        else:
            print("No history found.")

    @staticmethod
    def clear_history():
        # Clear the in-memory history and delete the file
        if os.path.exists(HistoryManager.file_name):
            os.remove(HistoryManager.file_name)
            print("History cleared.")
        else:
            print("No history to clear.")

    @staticmethod
    def delete_record(index):
        if os.path.exists(HistoryManager.file_name):
            try: 
                history = pd.read_csv(HistoryManager.file_name)
                index = int(index)
                
                if 0 <= index < len(history):
                    history = history.drop(history.index[index])
                    history.to_csv(HistoryManager.file_name, index=False)
                    print(f"Record at position {index} deleted.")
                else:
                    print(f"Record at position {index} not found. Valid positions are 0 to {len(history)-1}.")
            except Exception as e:
                print(f"Error deleting record: {e}")
        else:
            print("No history file exists.")

    @staticmethod
    def save_history(): 
        """Saving the history of the CSV"""
        if os.path.exists(HistoryManager.file_name):
            history = pd.read_csv(HistoryManager.file_name)
        else:
            history = pd.DataFrame(columns=['Operation', 'Num1', 'Num2', 'Result'])
        
        history.to_csv(HistoryManager.file_name, index=False)
        print("Saved Sucessfully")

    @staticmethod
    def display_history():
        """Display the history of the CSV"""
        if os.path.exists(HistoryManager.file_name):
            history = pd.read_csv(HistoryManager.file_name)
            if history.empty:
                print("No records in history.")
            else:
                print(history)
        else:
            print("No history found.")


# HistoryManager.add_record("add", 5, 5, 10)
# HistoryManager.display_history()
# HistoryManager.delete_record(0)
# HistoryManager.clear_history()
