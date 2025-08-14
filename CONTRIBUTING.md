# Contributing to MPMA

Thank you for your interest in contributing to the MCP Preference Manipulation Attack (MPMA) project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check if the issue already exists in the [GitHub Issues](https://github.com/cao-elaine/MPMA/issues)
2. If not, create a new issue with a clear title and description
3. Include steps to reproduce the issue if applicable
4. Add relevant labels

### Submitting Changes

1. Fork the repository
2. Create a new branch for your changes: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run tests if applicable
5. Commit your changes with clear commit messages
6. Push to your fork
7. Submit a pull request

### Pull Request Process

1. Ensure your code follows the project's coding standards
2. Update documentation as necessary
3. Include a clear description of the changes in your pull request
4. Link any related issues using keywords like "Fixes #123" or "Resolves #456"

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/cao-elaine/MPMA.git
cd MPMA
```

2. Create a Python virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up your API keys:
```bash
cp client/fastagent.secrets.template.yaml client/fastagent.secrets.yaml
```
Then edit `client/fastagent.secrets.yaml` to add your API keys.

## Coding Standards

- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused on a single task
- Write clear comments for complex logic

## Adding New MCP Servers

If you want to add a new MCP server type:

1. Create a new directory under `Servers/` with the server name
2. Implement the server following the existing patterns
3. Add appropriate entries to `config/configs.yaml`
4. Update the tool descriptions in `utils/tool_descriptions.json` if needed
5. Document the new server in the README.md

## Testing

Before submitting a pull request, please test your changes:

1. Run any existing tests
2. Test your changes with different inputs and edge cases
3. Ensure your changes don't break existing functionality

## Documentation

- Update documentation when you change code behavior
- Document new features thoroughly
- Keep the README.md up to date

## Questions?

If you have any questions about contributing, please open an issue for discussion.

Thank you for contributing to MPMA!
