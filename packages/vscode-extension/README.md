# VS Code Extension

VS Code extension for Component AI Agent with GitHub Copilot integration.

## Features

- **Copilot Integration**: Chat participant `@components` for component suggestions
- **Semantic Search**: Find components by description
- **Component Suggestions**: Get recommendations based on UI descriptions
- **Knowledge Base UI**: Sidebar for managing components
- **Auto-scanning**: Automatically index component folders on startup
- **RAG Service Management**: Start/stop the RAG service from VS Code

## Development

```bash
# Install dependencies
pnpm install

# Build
pnpm build

# Watch mode
pnpm dev

# Package extension
pnpm package
```

## Usage

### Copilot Chat

Use the `@components` participant in GitHub Copilot chat:

```
@components find a button component
@components suggest a component for a user profile card
@components explain the Button component
```

### Commands

- `Component AI: Scan Component Folder` - Scan and index a component folder
- `Component AI: Show Knowledge Base` - Open the sidebar
- `Component AI: Start RAG Service` - Manually start the RAG service
- `Component AI: Stop RAG Service` - Stop the RAG service
- `Component AI: Refresh Components` - Refresh the component list

### Configuration

```json
{
  "componentAI.ragService.port": 8765,
  "componentAI.ragService.autoStart": true,
  "componentAI.componentPaths": [
    "/path/to/your/components"
  ],
  "componentAI.embeddingModel": "all-MiniLM-L6-v2"
}
```

## Architecture

```
src/
├── extension.ts          # Extension entry point
├── copilot/
│   ├── agent.ts          # Copilot agent registration
│   └── tools.ts          # Tool definitions
├── rag-client/
│   └── client.ts         # RAG service HTTP client
├── sidebar/
│   └── provider.ts       # Webview provider for sidebar
└── utils/
    └── service-manager.ts # RAG service lifecycle management
```

## Building the Extension

The extension is bundled using webpack:

```bash
pnpm build
```

This creates a `dist/extension.js` file that can be loaded by VS Code.

## Testing

To test the extension:

1. Open the project in VS Code
2. Press F5 to start debugging
3. A new VS Code window will open with the extension loaded
4. Use the Copilot chat or commands to test functionality

