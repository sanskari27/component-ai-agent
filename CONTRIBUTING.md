# Contributing to Component AI Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Node.js >= 18.0.0
- PNPM >= 8.0.0
- Python >= 3.11
- VS Code >= 1.85.0

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd component-ai-agent

# Install dependencies
pnpm install

# Set up Python environment
cd packages/rag-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Build the project
pnpm build
```

## Project Structure

```
component-ai-agent/
├── packages/
│   ├── vscode-extension/    # VS Code extension
│   ├── rag-service/          # Python RAG service
│   └── shared-types/         # Shared TypeScript types
├── tools/                    # Build tools
└── README.md
```

## Development Workflow

### Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Test your changes:
   ```bash
   # TypeScript
   pnpm lint
   pnpm test
   
   # Python
   cd packages/rag-service
   pytest
   black src/
   ruff check src/
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```

### Commit Message Format

Use conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

### Testing

#### TypeScript/Extension

```bash
# Run linting
pnpm lint

# Build
pnpm build

# Test in VS Code
# Press F5 in VS Code to launch extension in debug mode
```

#### Python/RAG Service

```bash
cd packages/rag-service

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/
```

## Architecture Guidelines

### TypeScript

- Use TypeScript strict mode
- Follow existing code style (ESLint + Prettier)
- Add JSDoc comments for public APIs
- Use async/await for asynchronous code

### Python

- Follow PEP 8 style guide
- Use type hints
- Add docstrings for classes and functions
- Use Black for formatting
- Use Ruff for linting

### Adding New Features

#### Adding a New Copilot Tool

1. Define the tool in `packages/vscode-extension/src/copilot/tools.ts`
2. Implement the handler function
3. Add the tool to `allTools` array
4. Update documentation

#### Adding a New API Endpoint

1. Create route in `packages/rag-service/src/api/routes/`
2. Add Pydantic models in `packages/rag-service/src/api/models.py`
3. Include router in `main.py`
4. Add tests in `tests/`
5. Update API documentation

#### Adding Component Intelligence Features

1. Implement in `packages/rag-service/src/intelligence/`
2. Integrate with scanner or metadata extractor
3. Add tests
4. Update RAG pipeline if needed

## Code Review Process

1. Ensure all tests pass
2. Ensure code is formatted and linted
3. Update documentation if needed
4. Submit pull request
5. Address review feedback

## Documentation

- Update README.md for major changes
- Add/update docstrings and comments
- Update GETTING_STARTED.md for user-facing changes
- Add examples for new features

## Release Process

1. Update version in package.json files
2. Update CHANGELOG.md
3. Create release tag
4. Build and package extension
5. Publish to VS Code Marketplace (if applicable)

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about the codebase
- Suggestions for improvements

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

