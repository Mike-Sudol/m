import pandas as pd
import os

class HistoryManager:
    def __init__(self, file_name='history.csv'):
        self.file_name = file_name
        # Load existing history if the file exists, otherwise create an empty dataframe
        if os.path.exists(self.file_name):
            self.history = pd.read_csv(self.file_name)
        else:
            # Set columns as operation, num1, num2
            self.history = pd.DataFrame(columns=['Operation', 'Num1', 'Num2', 'Result'])

    def add_record(self, operation, num1, num2, result):
        # Add a new record with operation and numbers
        new_record = {'Operation': operation, 'Num1': num1, 'Num2': num2, 'Result': result}
        self.history = self.history.append(new_record, ignore_index=True)
        self.save_history()

    def save_history(self):
        # Save the history to the CSV file
        self.history.to_csv(self.file_name, index=False)

    def load_history(self):
        # Load history from the CSV file if it exists
        if os.path.exists(self.file_name):
            self.history = pd.read_csv(self.file_name)
            print("History loaded successfully.")
        else:
            print("No history found.")
    
    def clear_history(self):
        # Clear the in-memory history and delete the file
        self.history = pd.DataFrame(columns=['Operation', 'Num1', 'Num2', 'Result'])
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        print("History cleared.")

    def delete_record(self, index):
        # Delete a specific record by its index
        if index in self.history.index:
            self.history = self.history.drop(index)
            self.save_history()
            print(f"Record at index {index} deleted.")
        else:
            print(f"Record at index {index} not found.")

    def display_history(self):
        # Display the current history in memory
        if self.history.empty:
            print("No records in history.")
        else:
            print(self.history)


# history_manager = HistoryManager()
# history_manager.add_record("addition", 5, 5, 10)
# history_manager.display_history()
# history_manager.delete_record(0)
# history_manager.clear_history()
