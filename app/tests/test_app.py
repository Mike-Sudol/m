"""Test the main App"""
from unittest.mock import patch, MagicMock
import pytest
from app import App
from app.commands import Command, CommandHandler
from app.history import HistoryManager

class MockCommand(Command):
    """Mock command class for testing"""
    def execute(self, *args):
        return "mock executed"

@pytest.fixture
def app():
    """
    Fixture that provides a fresh App instance for each test.
    
    Returns:
        App: A fresh instance of the App class
    """
    with patch('os.makedirs'), \
         patch('logging.config.fileConfig'), \
         patch('dotenv.load_dotenv'):
        return App()

@pytest.fixture
def mock_env_vars():
    """
    Fixture that provides mock environment variables.
    
    Returns:
        dict: A dictionary of mock environment variables
    """
    return {
        'ENVIRONMENT': 'TEST',
        'DATA_DIR': '/test/data',
        'TEST_VAR': 'test_value'
    }

class TestApp:
    """Test suite for the App class"""

    def test_init(self, app):
        """
        Test that App initializes correctly with all required attributes.
        
        Args:
            app: Fixture providing App instance
        """
        assert isinstance(app.command_handler, CommandHandler)
        assert isinstance(app.history, HistoryManager)
        assert isinstance(app.settings, dict)
        assert app.settings.get('ENVIRONMENT') == 'PRODUCTION'

    @patch.dict('os.environ', {'ENVIRONMENT': 'TEST', 'DATA_DIR': '/test/data'})
    def test_load_environment_variables(self, app):
        """
        Test that environment variables are loaded correctly.
        
        Args:
            app: Fixture providing App instance
        """
        settings = app.load_environment_variables()
        assert settings['ENVIRONMENT'] == 'TEST'
        assert settings['DATA_DIR'] == '/test/data'

    def test_get_environment_variable(self, app):
        """
        Test retrieval of environment variables.
        
        Args:
            app: Fixture providing App instance
        """
        app.settings = {'TEST_VAR': 'test_value'}
        assert app.get_environment_variable('TEST_VAR') == 'test_value'
        assert app.get_environment_variable('NON_EXISTENT') is None

    @patch('pkgutil.iter_modules')
    @patch('importlib.import_module')
    def test_load_plugins(self, mock_import_module, mock_iter_modules, app):
        """
        Test plugin loading functionality.
        
        Args:
            mock_import_module: Mock for importlib.import_module
            mock_iter_modules: Mock for pkgutil.iter_modules
            app: Fixture providing App instance
        """
        # Mock plugin discovery
        mock_iter_modules.return_value = [
            (None, "test_plugin", True)
        ]
        # Mock plugin module with command
        mock_module = MagicMock()
        mock_module.TestCommand = MockCommand
        mock_import_module.return_value = mock_module

        with patch('os.path.exists', return_value=True):
            app.load_plugins()

    @patch('builtins.input', side_effect=['menu', 'exit'])
    def test_start(self, mock_input, app):
        """
        Test application start and command execution.
        
        Args:
            mock_input: Mock for input function
            app: Fixture providing App instance
        """
        with pytest.raises(SystemExit):
            app.start()

    def test_error_handling(self, app):
        """
        Test custom error handling.
        
        Args:
            app: Fixture providing App instance
        """
        with pytest.raises(App.Error):
            raise App.Error("Test error")

    @patch('logging.config.fileConfig')
    def test_configure_logging_with_config_file(self, mock_fileConfig, app):
        """
        Test logging configuration with existing config file.
        
        Args:
            mock_fileConfig: Mock for logging.config.fileConfig
            app: Fixture providing App instance
        """
        with patch('os.path.exists', return_value=True):
            app.configure_logging()
            mock_fileConfig.assert_called_once()

    def test_configure_logging_without_config_file(self, app):
        """
        Test logging configuration without config file.
        
        Args:
            app: Fixture providing App instance
        """
        with patch('os.path.exists', return_value=False), \
             patch('logging.basicConfig') as mock_basic_config:
            app.configure_logging()
            mock_basic_config.assert_called_once()

    def test_register_plugin_commands(self, app):
        """
        Test plugin command registration.
        
        Args:
            app: Fixture providing App instance
        """
        # Create mock plugin module
        mock_module = MagicMock()
        mock_module.TestCommand = MockCommand

        app.register_plugin_commands(mock_module, "test_plugin")

if __name__ == '__main__':
    pytest.main(['-v'])
