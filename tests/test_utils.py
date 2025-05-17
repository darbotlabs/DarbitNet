import unittest
from unittest.mock import patch

from utils.e2e_benchmark import run_command


class RunCommandTest(unittest.TestCase):
    @patch('utils.e2e_benchmark.sys.exit')
    @patch('utils.e2e_benchmark.subprocess.run')
    def test_run_command_success_no_exit(self, mock_run, mock_exit):
        mock_run.return_value = None
        run_command(['echo', 'hello'])
        mock_exit.assert_not_called()


if __name__ == '__main__':
    unittest.main()
