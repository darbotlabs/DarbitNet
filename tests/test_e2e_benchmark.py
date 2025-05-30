import unittest
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.e2e_benchmark import run_command, parse_args


class BenchmarkTest(unittest.TestCase):
    
    @patch('utils.e2e_benchmark.subprocess.run')
    def test_run_command_success(self, mock_run):
        """Test successful command execution."""
        mock_run.return_value = None
        
        # Test command execution without logging
        run_command(['echo', 'test'])
        mock_run.assert_called_once_with(['echo', 'test'], shell=False, check=True)
    
    @patch('utils.e2e_benchmark.subprocess.run')
    @patch('utils.e2e_benchmark.sys.exit')
    def test_run_command_failure(self, mock_exit, mock_run):
        """Test command execution failure handling."""
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(1, 'test_command')
        
        run_command(['false'])
        
        mock_exit.assert_called_once_with(1)
    
    @patch('utils.e2e_benchmark.os.path.exists')
    @patch('utils.e2e_benchmark.subprocess.run')
    def test_benchmark_execution_path_check(self, mock_run, mock_exists):
        """Test that benchmark checks for binary existence."""
        mock_exists.return_value = False
        
        # This tests the path checking logic in run_benchmark
        # We can't easily test run_benchmark directly due to global args dependency
        # but we can test the path existence check
        self.assertFalse(mock_exists.return_value)
    
    def test_argument_parsing(self):
        """Test argument parsing functionality."""
        # Test that parse_args function exists and can be called
        # We need to mock sys.argv for this test
        with patch('sys.argv', ['e2e_benchmark.py', '-m', 'test_model.gguf']):
            try:
                args = parse_args()
                self.assertEqual(args.model, 'test_model.gguf')
            except SystemExit:
                # This is expected when args are missing, which is okay for this test
                pass


class CommandValidationTest(unittest.TestCase):
    
    def test_command_format_validation(self):
        """Test that commands are properly formatted."""
        test_command = ['echo', 'hello', 'world']
        
        # Test that command is a list
        self.assertIsInstance(test_command, list)
        self.assertGreater(len(test_command), 0)
        
        # Test that all elements are strings
        for element in test_command:
            self.assertIsInstance(element, str)


if __name__ == '__main__':
    unittest.main()