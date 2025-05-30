import unittest
import os
import sys
import tempfile
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class InferenceScriptTest(unittest.TestCase):
    
    def test_inference_script_exists(self):
        """Test that inference scripts exist and are readable."""
        project_root = Path(__file__).parent.parent
        
        run_inference_path = project_root / "run_inference.py"
        run_inference_server_path = project_root / "run_inference_server.py"
        
        self.assertTrue(run_inference_path.exists(), "run_inference.py should exist")
        self.assertTrue(run_inference_server_path.exists(), "run_inference_server.py should exist")
        
        # Test that files are readable
        with open(run_inference_path, 'r') as f:
            content = f.read()
            self.assertIn("argparse", content, "Should use argparse for CLI")
            self.assertIn("import", content, "Should have imports")


class UtilsScriptTest(unittest.TestCase):
    
    def test_utility_scripts_exist(self):
        """Test that utility scripts exist."""
        project_root = Path(__file__).parent.parent
        utils_dir = project_root / "utils"
        
        expected_scripts = [
            "e2e_benchmark.py",
            "convert-hf-to-gguf-bitnet.py",
            "generate-dummy-bitnet-model.py",
            "kernel_tuning.py",
            "codegen_tl1.py",
            "codegen_tl2.py"
        ]
        
        for script in expected_scripts:
            script_path = utils_dir / script
            self.assertTrue(script_path.exists(), f"{script} should exist in utils/")
    
    def test_utils_have_proper_structure(self):
        """Test that utility scripts have basic Python structure."""
        project_root = Path(__file__).parent.parent
        utils_dir = project_root / "utils"
        
        # Test e2e_benchmark.py specifically since it's most used
        benchmark_path = utils_dir / "e2e_benchmark.py"
        
        with open(benchmark_path, 'r') as f:
            content = f.read()
            self.assertIn("import", content, "Should have imports")
            self.assertIn("def ", content, "Should have function definitions")


class ProjectStructureTest(unittest.TestCase):
    
    def test_required_directories_exist(self):
        """Test that required project directories exist."""
        project_root = Path(__file__).parent.parent
        
        required_dirs = [
            "src",
            "tests", 
            "utils",
            "docs",
            "3rdparty",
            "include",
            "preset_kernels"
        ]
        
        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            self.assertTrue(dir_path.exists(), f"Directory {dir_name} should exist")
            self.assertTrue(dir_path.is_dir(), f"{dir_name} should be a directory")
    
    def test_configuration_files_exist(self):
        """Test that important configuration files exist."""
        project_root = Path(__file__).parent.parent
        
        config_files = [
            "CMakeLists.txt",
            "requirements.txt",
            "setup_env.py",
            "README.md",
            "LICENSE",
            ".gitignore",
            ".gitmodules"
        ]
        
        for file_name in config_files:
            file_path = project_root / file_name
            self.assertTrue(file_path.exists(), f"Configuration file {file_name} should exist")
            self.assertTrue(file_path.is_file(), f"{file_name} should be a file")


if __name__ == '__main__':
    unittest.main()