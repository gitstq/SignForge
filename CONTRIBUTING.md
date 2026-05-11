# Contributing to SignForge

Thank you for your interest in contributing to SignForge! 🎉

## How to Contribute

### Reporting Bugs
1. Check if the bug has already been reported in [Issues](https://github.com/gitstq/SignForge/issues)
2. If not, create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version)

### Submitting Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Write your code with clear comments
4. Add tests for new functionality
5. Ensure all tests pass: `python -m pytest tests/`
6. Commit with conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`
7. Push and create a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to all public functions/classes
- Keep functions focused and small
- Add type hints where appropriate

## Development Setup

```bash
git clone https://github.com/gitstq/SignForge.git
cd SignForge
pip install -e ".[dev]"
python -m pytest tests/
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
