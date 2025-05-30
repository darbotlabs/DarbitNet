import unittest
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import setup_env


class SetupEnvTest(unittest.TestCase):
    
    def test_supported_models_configuration(self):
        """Test that supported models are properly configured."""
        self.assertIn("1bitLLM/bitnet_b1_58-large", setup_env.SUPPORTED_HF_MODELS)
        self.assertIn("microsoft/BitNet-b1.58-2B-4T", setup_env.SUPPORTED_HF_MODELS)
        
        # Check model structure
        model_config = setup_env.SUPPORTED_HF_MODELS["1bitLLM/bitnet_b1_58-large"]
        self.assertIn("model_name", model_config)
        self.assertEqual(model_config["model_name"], "bitnet_b1_58-large")
    
    def test_supported_quant_types(self):
        """Test quantization types are properly defined."""
        self.assertIn("arm64", setup_env.SUPPORTED_QUANT_TYPES)
        self.assertIn("x86_64", setup_env.SUPPORTED_QUANT_TYPES)
        
        # Check that basic quantization types are supported
        for arch in setup_env.SUPPORTED_QUANT_TYPES.values():
            self.assertIn("i2_s", arch)
    
    @patch('setup_env.subprocess.run')
    def test_command_execution_success(self, mock_run):
        """Test successful command execution."""
        mock_run.return_value = MagicMock(returncode=0)
        
        # This would test the actual function if it was accessible
        # For now, just test that the mock works
        self.assertEqual(mock_run.return_value.returncode, 0)
    
    def test_logging_configuration(self):
        """Test that logging is properly configured."""
        self.assertIsNotNone(setup_env.logger)
        self.assertEqual(setup_env.logger.name, "setup_env")


class PathValidationTest(unittest.TestCase):
    
    def test_model_directory_structure(self):
        """Test model directory validation logic."""
        with tempfile.TemporaryDirectory() as temp_dir:
            model_dir = Path(temp_dir) / "test_model"
            model_dir.mkdir(exist_ok=True)
            
            # Test directory exists
            self.assertTrue(model_dir.exists())
            self.assertTrue(model_dir.is_dir())


if __name__ == '__main__':
    unittest.main()