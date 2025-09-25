#!/usr/bin/env python3
"""
Test module for Copilot instructions configuration.
"""

import os
import unittest
from pathlib import Path


class CopilotInstructionsTest(unittest.TestCase):
    """Test cases for Copilot instructions file."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo_root = Path(__file__).parent.parent
        self.copilot_file = self.repo_root / ".github" / "copilot-instructions.md"

    def test_copilot_instructions_file_exists(self):
        """Test that the Copilot instructions file exists."""
        self.assertTrue(
            self.copilot_file.exists(),
            f"Copilot instructions file not found at {self.copilot_file}"
        )

    def test_copilot_instructions_has_required_sections(self):
        """Test that the Copilot instructions contain required sections."""
        content = self.copilot_file.read_text(encoding='utf-8')
        
        required_sections = [
            "# GitHub Copilot Instructions for DarbitNet",
            "## Project Overview",
            "## Development Environment",
            "## Code Standards & Guidelines",
            "## Validation Requirements",
            "## Common Development Tasks",
            "## Architecture Context",
            "## Testing Strategy"
        ]
        
        for section in required_sections:
            self.assertIn(
                section, content,
                f"Required section '{section}' not found in copilot instructions"
            )

    def test_copilot_instructions_mentions_darbitnet(self):
        """Test that the instructions properly reference DarbitNet."""
        content = self.copilot_file.read_text(encoding='utf-8')
        self.assertIn("DarbitNet", content)
        self.assertIn("BitNet", content)

    def test_copilot_instructions_includes_build_info(self):
        """Test that build and validation information is included."""
        content = self.copilot_file.read_text(encoding='utf-8')
        
        build_related_terms = [
            "cmake",
            "pytest",
            "flake8",
            "C++",
            "Python"
        ]
        
        for term in build_related_terms:
            self.assertIn(
                term.lower(), content.lower(),
                f"Build-related term '{term}' not found in instructions"
            )

    def test_copilot_instructions_has_validation_commands(self):
        """Test that validation commands are properly documented."""
        content = self.copilot_file.read_text(encoding='utf-8')
        
        validation_commands = [
            "ctest --output-on-failure",
            "flake8",
            "pytest"
        ]
        
        for command in validation_commands:
            self.assertIn(
                command, content,
                f"Validation command '{command}' not found in instructions"
            )


if __name__ == '__main__':
    unittest.main()