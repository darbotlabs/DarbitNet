# Contributing to DarbitNet

Thank you for your interest in contributing to DarbitNet! This document provides guidelines and information for contributors.

## Code of Conduct

This project follows the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). Please read and follow these guidelines.

## Getting Started

### Prerequisites

- Python 3.9 or later
- CMake 3.22 or later
- Clang 18 or later
- Git with submodule support

### Development Setup

1. **Clone the repository with submodules:**
   ```bash
   git clone --recursive https://github.com/darbotlabs/DarbitNet.git
   cd DarbitNet
   ```

2. **Set up Python environment:**
   ```bash
   # Create virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install pytest flake8 bandit safety  # Development tools
   ```

3. **Build the project:**
   ```bash
   cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
   cmake --build build --config Release
   ```

4. **Run tests:**
   ```bash
   python -m pytest tests/ -v
   ```

## Development Workflow

### 1. Before Making Changes

- Check existing issues and pull requests
- Create an issue for new features or bugs
- Fork the repository and create a feature branch

### 2. Making Changes

#### Code Style
- Follow PEP 8 for Python code
- Use descriptive variable and function names
- Add docstrings for public functions and classes
- Keep functions focused and small

#### Testing
- Write tests for new functionality
- Ensure all existing tests pass
- Aim for good test coverage
- Test on multiple platforms when possible

#### Security
- Follow secure coding practices
- Don't commit sensitive information
- Use security tools (bandit, safety) before submitting

### 3. Pre-commit Checklist

Run these commands before committing:

```bash
# Lint Python code
flake8 .

# Security scan
bandit -r . --exclude tests,3rdparty

# Run all tests
python -m pytest tests/ -v

# Check dependencies for vulnerabilities
safety check
```

### 4. Commit Guidelines

- Use clear, descriptive commit messages
- Reference issue numbers in commits
- Keep commits focused on single changes
- Use conventional commit format when possible:
  ```
  feat: add new model support
  fix: resolve memory leak in inference
  docs: update installation instructions
  test: add benchmark validation tests
  ```

### 5. Pull Request Process

1. **Create a Pull Request:**
   - Use a descriptive title
   - Fill out the PR template
   - Link related issues
   - Add reviewers if known

2. **PR Requirements:**
   - All CI checks must pass
   - Code review approval required
   - Tests must pass on all platforms
   - Documentation updated if needed

3. **Review Process:**
   - Address feedback promptly
   - Keep discussions respectful
   - Update PR based on feedback

## Types of Contributions

### 🐛 Bug Reports
- Use the bug report template
- Include minimal reproduction steps
- Provide environment details
- Search existing issues first

### 💡 Feature Requests
- Use the feature request template
- Explain the use case clearly
- Consider implementation complexity
- Discuss in issues before large changes

### 📝 Documentation
- Improve existing documentation
- Add missing API documentation
- Update installation guides
- Fix typos and formatting

### 🧪 Testing
- Add missing test coverage
- Improve test quality
- Add integration tests
- Performance testing

### 🔧 Code Contributions
- Bug fixes
- Performance improvements
- New features (discuss first)
- Code refactoring

## Project Structure

```
DarbitNet/
├── .github/          # GitHub workflows and templates
├── 3rdparty/         # Third-party dependencies (submodules)
├── darbot-src/       # Windows-specific utilities
├── docs/             # Documentation
├── include/          # C++ header files
├── preset_kernels/   # Pre-built kernel configurations
├── src/              # C++ source code
├── tests/            # Test suite
├── utils/            # Python utilities and scripts
├── CMakeLists.txt    # Build configuration
├── requirements.txt  # Python dependencies
└── setup_env.py      # Environment setup script
```

## Coding Standards

### Python Code
- Follow PEP 8 style guide
- Use type hints where appropriate
- Maximum line length: 88 characters
- Use meaningful variable names
- Add docstrings for public functions

### C++ Code
- Follow Google C++ Style Guide
- Use modern C++ features (C++17)
- Consistent naming conventions
- Include appropriate headers
- Memory safety practices

### Documentation
- Write clear, concise documentation
- Include code examples
- Update README when adding features
- Use proper markdown formatting

## Testing Guidelines

### Test Categories
1. **Unit Tests**: Test individual functions/classes
2. **Integration Tests**: Test component interactions
3. **Performance Tests**: Benchmark critical paths
4. **Security Tests**: Validate security measures

### Test Requirements
- Tests must be deterministic
- No external dependencies in unit tests
- Clear test names and descriptions
- Good assertion messages
- Test edge cases and error conditions

## Security Guidelines

### Secure Coding
- Validate all inputs
- Handle errors gracefully
- Avoid hardcoded credentials
- Use secure communication protocols
- Follow principle of least privilege

### Reporting Security Issues
- **DO NOT** report security issues publicly
- Email security@darbotlabs.com
- Include detailed reproduction steps
- Allow time for responsible disclosure

## Performance Considerations

- Profile before optimizing
- Consider memory usage
- Test on target hardware
- Benchmark performance changes
- Document performance implications

## Documentation Standards

### Code Documentation
- Use clear, descriptive comments
- Document complex algorithms
- Explain non-obvious code sections
- Keep comments up-to-date

### API Documentation
- Document all public interfaces
- Include usage examples
- Specify parameter types and ranges
- Document return values and exceptions

## Release Process

1. **Version Planning**
   - Feature freeze period
   - Testing and bug fixing
   - Documentation updates

2. **Release Preparation**
   - Update version numbers
   - Create release notes
   - Final testing round

3. **Release Execution**
   - Create release branch
   - Tag release version
   - Deploy release artifacts

## Getting Help

### Communication Channels
- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and ideas
- Email: security@darbotlabs.com (security issues only)

### Documentation
- README.md: Project overview and quick start
- docs/: Detailed documentation
- Code comments: Implementation details
- GitHub Wiki: Additional resources

## Recognition

Contributors will be acknowledged in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributor graph
- Special recognition for significant contributions

## License

By contributing to DarbitNet, you agree that your contributions will be licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Thank you for contributing to DarbitNet! Your efforts help make 1-bit LLM inference accessible to everyone.