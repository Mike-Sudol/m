"""Tests the main App"""
import os
import logging
from unittest import mock
import pytest
from app import App

@pytest.fixture
def mock_env_and_files(tmpdir, monkeypatch):
    """Fixture to mock the environment variables and file system operations."""
    monkeypatch.setattr(os, 'makedirs', mock.Mock())
    monkeypatch.setattr('dotenv.load_dotenv', mock.Mock())
    mock_env = {
        'ENVIRONMENT': 'TEST',
        'DATA_DIR': str(tmpdir)
    }
    monkeypatch.setattr(os, 'environ', mock_env)
    monkeypatch.setattr(logging, 'info', mock.Mock())

@pytest.fixture
def app(mock_env_and_files):
    """Fixture to create an instance of the App class with mocked environment and file system."""
    return App()

def test_app_initialization(app):
    """Test if App initialization sets up the settings, command handler, and history correctly."""
    assert app.settings.get('ENVIRONMENT') == 'TEST'
    assert 'DATA_DIR' in app.settings
    assert app.command_handler is not None
    assert app.history is not None

def test_configure_logging(app, monkeypatch):
    """Test if the logging configuration is set up correctly when a configuration file exists."""
    monkeypatch.setattr(os.path, 'exists', lambda x: True)
    mock_logging_config = mock.Mock()
    monkeypatch.setattr('logging.config.fileConfig', mock_logging_config)
    app.configure_logging()
    mock_logging_config.assert_called_once()

def test_load_environment_variables(app):
    """Test if the environment variables are loaded correctly by the app."""
    assert app.get_environment_variable('ENVIRONMENT') == 'TEST'
    assert app.get_environment_variable('DATA_DIR') is not None

def test_get_environment_variable(app):
    """Test if the app returns None when fetching a non-existent environment variable."""
    assert app.get_environment_variable('NON_EXISTENT_VAR') is None

@mock.patch('app.pkgutil.iter_modules')
@mock.patch('app.importlib.import_module')
def test_load_plugins(mock_import_module, mock_iter_modules, app, monkeypatch):
    """Test the plugin loading mechanism of the app by mocking the plugin directory and module imports."""
    monkeypatch.setattr(os.path, 'exists', lambda x: True)
    mock_iter_modules.return_value = [
        (None, 'plugin1', True),
        (None, 'plugin2', True)
    ]
    mock_import_module.side_effect = lambda name: mock.Mock()
    app.load_plugins()
    mock_import_module.assert_any_call('app.plugins.plugin1')
    mock_import_module.assert_any_call('app.plugins.plugin2')
