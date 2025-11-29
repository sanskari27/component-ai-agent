# Component AI Agent

An AI-powered VS Code Copilot Agent that provides intelligent React component suggestions using a RAG pipeline powered by ChromaDB.

## Overview

This project enables GitHub Copilot to provide context-aware code completions based on your custom React component library. Instead of suggesting generic HTML or unrelated components, it uses a local knowledge base and vector search to recommend the right components from your library.

## Architecture

- **VS Code Extension**: TypeScript-based extension with Copilot integration and sidebar UI
- **RAG Service**: Python FastAPI service with ChromaDB for semantic search
- **Shared Types**: Common TypeScript types across packages

## Monorepo Structure

```
component-ai-agent/
├── packages/
│   ├── vscode-extension/    # VS Code Extension
│   ├── rag-service/          # Python RAG Service
│   └── shared-types/         # Shared TypeScript types
├── tools/                    # Build tools and scripts
└── README.md
```

## Prerequisites

- Node.js >= 18.0.0
- PNPM >= 8.0.0
- Python >= 3.11
- VS Code >= 1.85.0

## Getting Started

### Installation

```bash
# Install dependencies
pnpm install

# Set up Python environment
cd packages/rag-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Development

```bash
# Build all packages
pnpm build

# Run in development mode
pnpm dev

# Run linting
pnpm lint

# Format code
pnpm format
```

### Running the Extension

1. Open the project in VS Code
2. Press F5 to start debugging
3. The extension will launch in a new VS Code window
4. The RAG service will start automatically on port 8765

## Features

- **Semantic Component Search**: Find components by description or functionality
- **Component Metadata**: Access props, types, and usage examples
- **Storybook Integration**: View component examples from Storybooks
- **Folder Scanning**: Automatically index your component library
- **Copilot Integration**: AI-powered suggestions using your components
- **Knowledge Base UI**: Manage components via VS Code sidebar

## Configuration

Configure the extension via VS Code settings:

```json
{
  "componentAI.ragService.port": 8765,
  "componentAI.ragService.autoStart": true,
  "componentAI.componentPaths": [],
  "componentAI.embeddingModel": "all-MiniLM-L6-v2"
}
```

## Contributing

This is a monorepo managed with PNPM workspaces. Each package has its own README with specific development instructions.

## License

MIT

