# Contributing to SentimentVault

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the SentimentVault project.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and adhere to our Code of Conduct.

## How to Contribute

### 1. Reporting Bugs

**Before submitting a bug report:**
- Check if the issue already exists in GitHub Issues
- Provide a clear description of the bug
- Include steps to reproduce the issue
- Provide expected vs. actual behavior
- Include your environment (OS, Python version, GPU/CPU)

**Bug Report Template:**
```
**Description:** Brief description of the bug

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior:** What should happen

**Actual Behavior:** What actually happened

**Environment:**
- OS: [e.g., macOS 13.0]
- Python: [e.g., 3.10.5]
- Device: [e.g., Apple Silicon M1]
```

### 2. Suggesting Enhancements

**Enhancement Suggestions:**
- Use GitHub Issues with `[FEATURE]` prefix
- Provide clear use case and benefits
- Include any relevant mockups or examples

**Enhancement Template:**
```
**Problem:** What problem does this solve?

**Solution:** Proposed solution

**Alternatives:** Any alternative approaches?

**Impact:** How would this benefit users?
```

### 3. Pull Requests

**Before Starting:**
1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

**PR Guidelines:**
- Link related issues: `Closes #123`
- Provide clear description of changes
- Include any new dependencies
- Update documentation if needed
- Ensure all tests pass

**PR Template:**
```
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Related Issues
Closes #123

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests passed
- [ ] Load tests passed (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Ready for review
```

## Development Setup

### Clone and Setup
```bash
git clone https://github.com/Abhishek17ak/SentimentVault.git
cd SentimentVault
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Install Development Tools
```bash
pip install pytest pytest-cov black flake8
```

### Running Tests
```bash
# Unit tests
pytest tests/

# With coverage
pytest tests/ --cov=backend

# Style checking
flake8 backend/ --max-line-length=100
black --check backend/
```

### Code Style

We follow PEP 8 with Black formatting:

```bash
# Auto-format code
black backend/ scripts/

# Check code style
flake8 backend/ scripts/
```

**Key Style Points:**
- Max line length: 100 characters
- Use type hints where possible
- Document functions with docstrings
- Use meaningful variable names
- Add comments for complex logic

## Git Workflow

### Branch Naming
- Feature: `feature/short-description`
- Bug fix: `bugfix/short-description`
- Documentation: `docs/short-description`

### Commit Messages
- Use present tense: "Add feature" not "Added feature"
- Be specific: "Fix cache timeout bug" not "Fix bug"
- Reference issues: "Closes #123"
- Example: `fix: reduce API latency by 20% (#456)`

### Commit Types
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style changes
- `refactor:` Code refactoring
- `perf:` Performance improvement
- `test:` Test addition/update

## Areas for Contribution

### High Priority
- [ ] Add unit tests for backend API
- [ ] Implement API authentication
- [ ] Add Kubernetes deployment manifests
- [ ] Performance optimizations

### Medium Priority
- [ ] Additional model variants (BERT, RoBERTa)
- [ ] Multi-language support
- [ ] Advanced caching strategies
- [ ] Enhanced monitoring/alerting

### Low Priority
- [ ] Documentation improvements
- [ ] Example scripts
- [ ] Helper utilities

## Testing Guidelines

### Unit Tests
```python
# tests/test_api.py
import pytest
from backend.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_predict_positive(client):
    response = client.post("/predict", json={
        "text": "Amazing product!"
    })
    assert response.status_code == 200
    assert response.json()["sentiment"] == "POSITIVE"
```

### Running Tests
```bash
# All tests
pytest

# Specific test file
pytest tests/test_api.py

# Specific test
pytest tests/test_api.py::test_predict_positive

# With verbose output
pytest -v

# With coverage
pytest --cov=backend --cov-report=html
```

## Documentation

### README Updates
- Keep installation instructions current
- Document new features
- Update architecture diagrams if needed

### Code Documentation
- Use docstrings for all functions
- Include type hints
- Provide usage examples

### API Documentation
- Maintain OpenAPI/Swagger specs
- Document all endpoints
- Include request/response examples

## Performance Contributions

When submitting performance improvements:
1. Benchmark before and after
2. Document the improvement
3. Include load testing results
4. Verify no regression on accuracy

Example:
```
**Latency Improvement: 25%**
- Before: 45ms average
- After: 34ms average
- Method: Reduced tokenizer overhead
- Load test: 5.2K req/hour ✓
```

## Review Process

1. **Automated Checks:**
   - Tests must pass
   - Code coverage >80%
   - No linting errors

2. **Code Review:**
   - At least 2 approvals required
   - Constructive feedback on changes
   - Discussion of design decisions

3. **Merge:**
   - Squash commits if needed
   - Merge to main branch
   - Close related issues

## Getting Help

- **Documentation:** Check README.md and docs/
- **Issues:** Search existing GitHub Issues
- **Discussions:** GitHub Discussions for questions
- **Email:** abhishek.kalugade@example.com

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing! 🙏
