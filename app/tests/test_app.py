import pytest
import os
import logging
from unittest.mock import patch, MagicMock
from app import App
from app.commands import Command, CommandHandler
from app.history import HistoryManager

class MockCommand(Command):
    """Mock command class for testing"""
    def execute(self, *args):
        return "mock executed"

@pytest.fixture
def mock_file_operations():
    """
    Fixture to mock file system operations.
    
    This fixture ensures all file operations are properly mocked,
    preventing issues with file system access during testing.
    """
    with patch('os.makedirs') as mock_makedirs, \
         patch('os.path.exists', return_value=True) as mock_exists, \
         patch('logging.config.fileConfig') as mock_config, \
         patch('dotenv.load_dotenv') as mock_dotenv:
        yield {
            'makedirs': mock_makedirs,
            'exists': mock_exists,
            'config': mock_config,
            'dotenv': mock_dotenv
        }

@pytest.fixture
def app(mock_file_operations):
    """
    Fixture that provides a fresh App instance for each test.
    
    Args:
        mock_file_operations: Fixture providing mocked file operations
    
    Returns:
        App: A fresh instance of the App class
    """
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

    def test_init(self, app, mock_file_operations):
        """
        Test that App initializes correctly with all required attributes.
        
        Args:
            app: Fixture providing App instance
            mock_file_operations: Fixture providing mocked file operations
        """
        assert isinstance(app.command_handler, CommandHandler)
        assert isinstance(app.history, HistoryManager)
        assert isinstance(app.settings, dict)
        assert app.settings.get('ENVIRONMENT') == 'PRODUCTION'
        mock_file_operations['makedirs'].assert_called_once_with('logs', exist_ok=True)

    @patch.dict('os.environ', {'ENVIRONMENT': 'TEST', 'DATA_DIR': '/test/data'})
    def test_load_environment_variables(self, app, mock_file_operations):
        """
        Test that environment variables are loaded correctly.
        
        Args:
            app: Fixture providing App instance
            mock_file_operations: Fixture providing mocked file operations
        """
        settings = app.load_environment_variables()
        assert settings['ENVIRONMENT'] == 'TEST'
        assert settings['DATA_DIR'] == '/test/data'

    def test_get_environment_variable(self, app, mock_file_operations):
        """
        Test retrieval of environment variables.
        
        Args:
            app: Fixture providing App instance
            mock_file_operations: Fixture providing mocked file operations
        """
        app.settings = {'TEST_VAR': 'test_value'}
        assert app.get_environment_variable('TEST_VAR') == 'test_value'
        assert app.get_environment_variable('NON_EXISTENT') is None

    @patch('pkgutil.iter_modules')
    @patch('importlib.import_module')
    def test_load_plugins(self, mock_import_module, mock_iter_modules, app, mock_file_operations):
        """
        Test plugin loading functionality.
        
        Args:
            mock_import_module: Mock for importlib.import_module
            mock_iter_modules: Mock for pkgutil.iter_modules
            app: Fixture providing App instance
            mock_file_operations: Fixture providing mocked file operations
        """
        # Mock plugin discovery
        mock_iter_modules.return_value = [
            (None, "test_plugin", True)
        ]
        
        # Mock plugin module with command
        mock_module = MagicMock()
        mock_module.TestCommand = MockCommand
        mock_import_module.return_value = mock_module

        app.load_plugins()
        mock_file_operations['exists'].assert_called()

    @patch('builtins.input', side_effect=['menu', 'exit'])
    def test_start(self, mock_input, app, mock_file_operations):
        """
        Test application start and command execution.
        
        Args:
            mock_input: Mock for input function
            app: Fixture providing App instance
            mock_file_operations: Fixture providing mocked file operations
        """
        with pytest.raises(SystemExit):
            app.start()

    def test_error_handling(self, app, mock_file_operations):
        """
        Test custom error handling.
        
        Args:
            app: Fixture providing App instance
            mock_file_operations: Fixture providing mocked file operations
        """
        with pytest.raises(App.Error):
            raise App.Error("Test error")

    def test_register_plugin_commands(self, app, mock_file_operations):
        """
        Test plugin command registration.
        
        Args:
            app: Fixture providing App instance
            mock_file_operations: Fixture providing mocked file operations
        """
        # Create mock plugin module
        mock_module = MagicMock()
        mock_module.TestCommand = MockCommand

        app.register_plugin_commands(mock_module, "test_plugin")

if __name__ == '__main__':
    pytest.main(['-v'])