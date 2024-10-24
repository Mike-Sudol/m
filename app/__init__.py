""" Main Application"""
import os
import pkgutil
import importlib
import logging
import logging.config
from dotenv import load_dotenv
from app.commands import Command, CommandHandler
from app.history import HistoryManager
from app.plugins.menu import MenuCommand


class App:
    """ Application Class """
    def __init__(self):
        """ Initialize """
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()
        self.history = HistoryManager()
        self.history.set_directory(self.get_environment_variable("DATA_DIR"))

    def configure_logging(self):
        """Configures logging"""
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

    def load_environment_variables(self):
        """Loads our environment vairables"""
        settings = dict(os.environ.items())
        logging.info("Environment variables loaded.")
        return settings
    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        """Fetches our environment vairables"""
        return self.settings.get(env_var, None)

    class Error(Exception):
        """Custom exception for bad input"""

    def load_plugins(self):
        """ Load Plugins """ 
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/')
        if not os.path.exists(plugins_path):
            logging.warning(f"Plugins directory '{plugins_path}' not found.")
            return
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    self.register_plugin_commands(plugin_module, plugin_name)
                except ImportError as e:
                    logging.error(f"Error importing plugin {plugin_name}: {e}")



    def register_plugin_commands(self, plugin_module, plugin_name):
        """Register a Plugin Command to the CLI"""
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                if plugin_name == "menu":
                    continue
                self.command_handler.register_command(plugin_name, item())
                logging.info(f"Command '{plugin_name}' from plugin '{plugin_name}' registered.")

    def start(self):
        """ Start Application """
        self.load_plugins()
        logging.info("Application started")
        print("Type 'menu' to see available commands, type 'exit' to quit")
        self.command_handler.register_command("menu", MenuCommand(self.command_handler))
        try:
            while True:
                user_input = input(">>> ").strip().split()
                if user_input:
                    command = user_input[0].lower()
                    args = user_input[1:]
                    result = self.command_handler.execute_command(command, args)
                    if command in ["add","subtract","divide","multiply"] and result is not None:
                        self.history.add_record(command, args[0], args[1], result)
        except App.Error as e:
            logging.info("Error while executing command %s",e)
        finally:
            logging.info("Application shutdown.")
