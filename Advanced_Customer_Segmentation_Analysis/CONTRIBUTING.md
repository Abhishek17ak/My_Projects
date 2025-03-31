# Contributing to Customer Segmentation Project

Thank you for considering contributing to this customer segmentation project! This document outlines the guidelines for contributing to this project.

## Code of Conduct

Please help keep this project open and inclusive. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

- **Use the GitHub issue tracker** to report bugs
- **Check if the bug has already been reported** before creating a new issue
- **Provide detailed information** about the bug:
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Screenshots if applicable
  - Your operating system and Python version

### Suggesting Enhancements

- **Use the GitHub issue tracker** with the "enhancement" label
- **Provide a clear and detailed explanation** of the feature/enhancement
- **Explain why this enhancement would be useful** to most users

### Pull Requests

1. **Fork the repository**
2. **Create a new branch** for your feature or bug fix
3. **Implement your changes**
4. **Write or update tests** if necessary
5. **Ensure your code passes all tests**
6. **Submit a pull request**

## Development Setup

### Setting up the development environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/customer_seg.git
cd customer_seg
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
pip install -e .  # Install the package in development mode
```

### Code Style Guidelines

- Follow **PEP 8** coding style guidelines
- Use **meaningful variable and function names**
- Include **docstrings** for all functions, classes, and modules
- Write **clear comments** for complex operations

### Testing

- Write tests for new features
- Ensure all tests pass before submitting a pull request
- Run tests using:
```bash
pytest
```

## Documentation

- Update documentation for new features or changes
- Use clear and concise language
- Include examples where appropriate

## Versioning

We use [Semantic Versioning](https://semver.org/) for this project:
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License. 