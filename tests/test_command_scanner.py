# tests/test_command_scanner.py

# TODO: to make this test work I have to upgrade my Python first; right now it's 2.7.16


import unittest
from unittest.mock import patch, MagicMock
from main.command_scanner import CommandsScanner  # Updated path

class TestCommandsScanner(unittest.TestCase):

    @patch('os.listdir')
    @patch('importlib.import_module')
    def test_get_command_instances(self, mock_import_module, mock_listdir):
        # Mock the files in the commands folder
        mock_listdir.return_value = ['start_command.py', 'hint_command.py', '__init__.py']
        
        # Mock the imported modules and their classes
        MockStartCommand = MagicMock()
        MockStartCommand.get_command_name.return_value = 'start'
        MockStartCommand.execute = MagicMock()

        MockHintCommand = MagicMock()
        MockHintCommand.get_command_name.return_value = 'hint'
        MockHintCommand.execute = MagicMock()

        # Set up the import_module mock to return these mock classes
        mock_import_module.side_effect = lambda name: {'start_command': MockStartCommand, 
                                                       'hint_command': MockHintCommand}.get(name.split('.')[-1])

        # Initialize CommandsScanner and get command instances
        scanner = CommandsScanner(commands_path='commands')
        command_instances = scanner.get_command_instances()

        # Assertions to verify correctness
        self.assertEqual(len(command_instances), 2)
        self.assertEqual(command_instances[0][0], 'start')
        self.assertEqual(command_instances[1][0], 'hint')
        self.assertIsInstance(command_instances[0][1], MagicMock)
        self.assertIsInstance(command_instances[1][1], MagicMock)

# Run the test
if __name__ == '__main__':
    unittest.main()
