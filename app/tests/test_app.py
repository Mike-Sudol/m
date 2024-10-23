import pytest
import os
import logging
from unittest import mock
from app import App

# Mocks the environment and file system calls
@pytest.fixture
def mock_env_and_files(tmpdir, monkeypatch):
    # Mocking os.makedirs
    monkeypatch.setattr(os, 'makedirs', mock.Mock())
    
    # Mocking dotenv loading
    monkeypatch.setattr('dotenv.load_dotenv', mock.Mock())
    
    # Mocking os.environ
    mock_env = {
        'ENVIRONMENT': 'TEST',
        'DATA_DIR': str(tmpdir)
    }
    monkeypatch.setattr(os, 'environ', mock_env)
    
    # Mock logging
    monkeypatch.setattr(logging, 'info', mock.Mock())

@pytest.fixture
def app(mock_env_and_files):
    return App()

def test_app_initialization(app):
    # Test if initialization sets up attributes properly
    assert app.settings.get('ENVIRONMENT') == 'TEST'
    assert 'DATA_DIR' in app.settings
    assert app.command_handler is not None
    assert app.history is not None

def test_configure_logging(app, monkeypatch):
    # Mock existence of logging configuration file
    monkeypatch.setattr(os.path, 'exists', lambda x: True)
    mock_logging_config = mock.Mock()
    monkeypatch.setattr('logging.config.fileConfig', mock_logging_config)
    
    # Re-run configure logging to see if it calls fileConfig when config file exists
    app.configure_logging()
    mock_logging_config.assert_called_once()

def test_load_environment_variables(app):
    # Check if environment variables are loaded correctly
    assert app.get_environment_variable('ENVIRONMENT') == 'TEST'
    assert app.get_environment_variable('DATA_DIR') is not None

def test_get_environment_variable(app):
    # Test fetching environment variables
    assert app.get_environment_variable('NON_EXISTENT_VAR') is None

@mock.patch('app.pkgutil.iter_modules')
@mock.patch('app.importlib.import_module')
def test_load_plugins(mock_import_module, mock_iter_modules, app, monkeypatch):
    # Mock the existence of plugins path
    monkeypatch.setattr(os.path, 'exists', lambda x: True)
    
    # Mock iter_modules to simulate plugin loading
    mock_iter_modules.return_value = [
        (None, 'plugin1', True),
        (None, 'plugin2', True)
    ]
    
    # Mock plugin module imports
    mock_import_module.side_effect = lambda name: mock.Mock()

    # Call load_plugins
    app.load_plugins()
    
    # Verify plugins were attempted to be loaded
    mock_import_module.assert_any_call('app.plugins.plugin1')
    mock_import_module.assert_any_call('app.plugins.plugin2')
