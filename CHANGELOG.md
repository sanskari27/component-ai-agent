# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-01

### Added

#### Core Features
- 🚀 GitHub Copilot integration with `@components` chat participant
- 🔍 Semantic search for React components
- 💡 AI-powered component suggestions based on UI descriptions
- 📚 Component knowledge base with sidebar UI
- 🤖 RAG pipeline with ChromaDB vector database
- 🔧 Automatic component folder scanning

#### VS Code Extension
- Copilot chat participant for component queries
- Sidebar webview for knowledge base management
- Commands for scanning, refreshing, and managing components
- Auto-start RAG service on activation
- Service lifecycle management

#### RAG Service
- FastAPI REST API for component operations
- ChromaDB integration for vector storage
- Sentence transformers for embeddings
- Component CRUD operations
- Semantic search and suggestions
- Health check endpoint

#### Component Intelligence
- TypeScript/TSX AST parsing
- Component metadata extraction
- Storybook file parsing
- Folder scanning with recursive support
- Props and type extraction

#### Developer Experience
- PNPM monorepo setup
- TypeScript shared types
- Comprehensive test suite
- ESLint and Prettier configuration
- Python Black and Ruff integration
- VS Code debug configurations

### Documentation
- Getting Started guide
- Contributing guidelines
- API documentation
- Architecture overview
- Development setup instructions

## [Unreleased]

### Planned Features
- Monorepo usage analysis
- Screenshot-based component similarity search
- Real-time component file watcher
- Analytics dashboard
- Theme variant suggestions
- Test snippet suggestions from Playwright
- Component usage frequency tracking

---

For more details on each release, see the [GitHub Releases](https://github.com/your-org/component-ai-agent/releases) page.

