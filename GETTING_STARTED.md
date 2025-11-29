# Component AI Agent - Getting Started Guide

This guide will help you set up and start using the Component AI Agent.

## Prerequisites

- **Node.js** >= 18.0.0
- **PNPM** >= 8.0.0
- **Python** >= 3.11
- **VS Code** >= 1.85.0
- **GitHub Copilot** subscription (for Copilot integration)

## Installation

### 1. Clone and Install Dependencies

```bash
# Install Node dependencies
pnpm install

# Install Python dependencies
cd packages/rag-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
cd ../..
```

### 2. Build the Project

```bash
# Build all packages
pnpm build
```

## Running the Extension

### Option 1: Debug Mode (Recommended for Development)

1. Open the project in VS Code
2. Press `F5` to start debugging
3. A new VS Code window will open with the extension loaded
4. The RAG service will start automatically

### Option 2: Install as Extension

```bash
# Package the extension
cd packages/vscode-extension
pnpm package

# Install the .vsix file
code --install-extension component-ai-agent-1.0.0.vsix
```

## Using the Extension

### 1. Index Your Component Library

First, you need to index your components:

**Method 1: Using Command Palette**
1. Open Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`)
2. Run: `Component AI: Scan Component Folder`
3. Select your component library folder

**Method 2: Using Configuration**
Add to your `.vscode/settings.json`:
```json
{
  "componentAI.componentPaths": [
    "/path/to/your/components"
  ]
}
```

The extension will automatically scan these paths on startup.

### 2. Use GitHub Copilot Chat

Open GitHub Copilot chat and use the `@components` participant:

```
@components find a button component

@components suggest a component for a user profile card

@components explain the Button component

@components search for form input components
```

### 3. Use the Knowledge Base Sidebar

1. Click on the Component AI icon in the Activity Bar
2. Browse indexed components
3. Search components by name or description
4. Click on a component to view details

## Configuration

Configure the extension in VS Code settings:

```json
{
  // RAG service port
  "componentAI.ragService.port": 8765,
  
  // Auto-start RAG service
  "componentAI.ragService.autoStart": true,
  
  // Component folders to auto-scan
  "componentAI.componentPaths": [
    "/path/to/your/components"
  ],
  
  // Embedding model
  "componentAI.embeddingModel": "all-MiniLM-L6-v2"
}
```

## Examples

### Example 1: Finding a Button Component

```
@components find a button component with primary variant
```

Response:
```
Found 3 components:

### PrimaryButton
A button component with primary styling

**Import:** `import { PrimaryButton } from 'components/Button';`

**Props:**
- `label`: string (required)
- `onClick`: () => void (required)
- `disabled`: boolean (optional)

**Example:**
```tsx
<PrimaryButton label="Click me" onClick={() => console.log('clicked')} />
```
```

### Example 2: Getting Component Suggestions

```
@components suggest a component for displaying user avatars
```

Response:
```
Here are 3 component suggestions:

### Avatar
Displays user profile pictures with fallback initials

**Import:** `import { Avatar } from 'components/Avatar';`

**Example usage:**
```tsx
<Avatar src="/profile.jpg" name="John Doe" size="large" />
```
```

### Example 3: Explaining a Component

```
@components explain the Card component
```

Response:
```
# Card

A flexible container component for grouping content

**Category:** Layout

**Import:**
```tsx
import { Card } from 'components/Card';
```

## Props

- **title**: `string` (optional)
  - Card title displayed in header
- **children**: `ReactNode` (required)
  - Card content
- **footer**: `ReactNode` (optional)
  - Card footer content

## Examples

### Basic Card
```tsx
<Card title="User Info">
  <p>Content goes here</p>
</Card>
```
```

## Troubleshooting

### RAG Service Won't Start

1. Check Python is installed: `python --version`
2. Check dependencies are installed: `pip list`
3. Check the Output panel: "Component AI" channel
4. Manually start the service:
   ```bash
   cd packages/rag-service
   python -m uvicorn src.main:app --reload --port 8765
   ```

### No Components Found

1. Ensure you've scanned your component folder
2. Check the folder contains `.tsx` or `.jsx` files
3. Check the Component AI output channel for scan errors
4. Try manually scanning: `Component AI: Scan Component Folder`

### Copilot Not Recognizing @components

1. Ensure GitHub Copilot extension is installed and active
2. Restart VS Code
3. Check that the extension is activated (look for "Component AI" in status bar)

## Advanced Usage

### Custom Embedding Model

You can use a different embedding model:

```json
{
  "componentAI.embeddingModel": "sentence-transformers/all-mpnet-base-v2"
}
```

### API Access

The RAG service exposes a REST API at `http://localhost:8765`:

```bash
# Search components
curl -X POST http://localhost:8765/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "button component", "limit": 5}'

# Get all components
curl http://localhost:8765/api/components

# Health check
curl http://localhost:8765/api/health
```

## Next Steps

- Index your component library
- Try the Copilot chat integration
- Explore the Knowledge Base sidebar
- Configure auto-scanning for your projects
- Integrate with your CI/CD pipeline

## Support

For issues or questions:
1. Check the Output panel: "Component AI" channel
2. Review the logs in the terminal
3. Open an issue on GitHub

## Development

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development guidelines.

