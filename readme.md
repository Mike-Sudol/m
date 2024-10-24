# IS601 Midterm

## How to Run

deactivate

pip install virtualenv 

pip install -r requirements.txt

virtualenv -p /usr/bin/python3 venv

source venv/bin/activate

pytest --cov

python3 main.py

## Commands

```
- add : num1 num2  Addition
- subtract : num1 num2 Subtraction
- multiply : num1 num2  Multiplication
- divide : num1 num2  Division
- talk : args Prints out arguments
- menu : Shows the list of commands
- exit : Exits the application
- display : Shows Calculation History
- load : Loads Calculation History from file
- save : Save Calculation History to file 
- delete : index Delete a record from Calculation History at an index
- clear : Clears Calculation History
```


## Video

Create a 3-5 minute video demonstration of using the calculator, highlighting its key features and functionalities. Link the video to the repository readme.

## Design Patterns

***Command Pattern***
wh
![commandPattern](images/CommandPattern.png)

***Singleton Pattern***

***Factory Method Pattern***

***Template Method Pattern***

***Iterator Pattern***



## LLBYL/EAFP

***"Look Before You Leap" (LBYL)***

if "possible_key" in data_dict:
    value = data_dict["possible_key"]
else:
    # Handle missing keys here...

***"Easier to Ask for Forgiveness than Permission" (EAFP)***

try:
     value = data_dict["possible_key"]
except KeyError:
    # Handle missing keys here...

## Logging

Dynamic logging configuration through environment variables is performed. A professional logging system is designed and logs will contain all the critical steps while performing any operation. Detailed application operations, data manipulations, errors, and informational messages are provided using Logging. This system also retrieves and displays errors and handles exceptions without crashing the applications. Logging is majorly used in this application rather than print statements.

- `logging.info`- logs what happened in the line of code
- `logging.error` - logs the error that occurred after the line of code

## Environment Variables

The application configuration details, development, and testing environment variables are stored in .env file.

https://github.com/karthikyeluripati/midterm_calculator/blob/f04dbbbde32de241a0cf74f8364f4667a5c635b7/app/__init__.py#L32-L41

## Testing 