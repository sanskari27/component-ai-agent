import * as vscode from 'vscode';
import { getRAGClient } from '../rag-client/client';
import { Component } from '@component-ai/shared-types';

export class KnowledgeBaseProvider implements vscode.WebviewViewProvider {
  private _view?: vscode.WebviewView;

  constructor(private readonly _extensionUri: vscode.Uri) {}

  public resolveWebviewView(
    webviewView: vscode.WebviewView,
    context: vscode.WebviewViewResolveContext,
    _token: vscode.CancellationToken
  ) {
    this._view = webviewView;

    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [this._extensionUri],
    };

    webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

    // Handle messages from the webview
    webviewView.webview.onDidReceiveMessage(async (data) => {
      switch (data.type) {
        case 'getComponents':
          await this.handleGetComponents();
          break;
        case 'searchComponents':
          await this.handleSearchComponents(data.query);
          break;
        case 'deleteComponent':
          await this.handleDeleteComponent(data.componentId);
          break;
        case 'scanFolder':
          await this.handleScanFolder();
          break;
        case 'showComponent':
          await this.handleShowComponent(data.component);
          break;
      }
    });

    // Load components on view creation
    this.loadComponents();
  }

  public refresh() {
    this.loadComponents();
  }

  private async loadComponents() {
    try {
      const client = getRAGClient();
      const components = await client.getAllComponents();
      this._view?.webview.postMessage({
        type: 'componentsLoaded',
        components,
      });
    } catch (error) {
      this._view?.webview.postMessage({
        type: 'error',
        message: `Failed to load components: ${error}`,
      });
    }
  }

  private async handleGetComponents() {
    await this.loadComponents();
  }

  private async handleSearchComponents(query: string) {
    try {
      const client = getRAGClient();
      const result = await client.searchComponents({ query, limit: 20 });
      this._view?.webview.postMessage({
        type: 'searchResults',
        results: result.results.map((r) => r.component),
      });
    } catch (error) {
      this._view?.webview.postMessage({
        type: 'error',
        message: `Search failed: ${error}`,
      });
    }
  }

  private async handleDeleteComponent(componentId: string) {
    try {
      const client = getRAGClient();
      await client.deleteComponent(componentId);
      this._view?.webview.postMessage({
        type: 'componentDeleted',
        componentId,
      });
      await this.loadComponents();
      vscode.window.showInformationMessage('Component deleted');
    } catch (error) {
      vscode.window.showErrorMessage(`Failed to delete component: ${error}`);
    }
  }

  private async handleScanFolder() {
    await vscode.commands.executeCommand('component-ai.scanFolder');
  }

  private async handleShowComponent(component: Component) {
    // Show component details in a new editor
    const doc = await vscode.workspace.openTextDocument({
      content: this.formatComponentDetails(component),
      language: 'markdown',
    });
    await vscode.window.showTextDocument(doc);
  }

  private formatComponentDetails(component: Component): string {
    let content = `# ${component.name}\n\n`;
    content += `${component.description}\n\n`;

    if (component.category) {
      content += `**Category:** ${component.category}\n\n`;
    }

    if (component.file_path) {
      content += `**File:** \`${component.file_path}\`\n\n`;
    }

    if (component.import_path) {
      content += `**Import:**\n\`\`\`tsx\nimport { ${component.name} } from '${component.import_path}';\n\`\`\`\n\n`;
    }

    if (component.props && component.props.length > 0) {
      content += `## Props\n\n`;
      for (const prop of component.props) {
        content += `- **${prop.name}**: \`${prop.type}\`${prop.required ? ' (required)' : ' (optional)'}\n`;
        if (prop.description) {
          content += `  ${prop.description}\n`;
        }
      }
      content += '\n';
    }

    if (component.examples && component.examples.length > 0) {
      content += `## Examples\n\n`;
      for (const example of component.examples) {
        content += `### ${example.title}\n\n`;
        if (example.description) {
          content += `${example.description}\n\n`;
        }
        content += `\`\`\`tsx\n${example.code}\n\`\`\`\n\n`;
      }
    }

    if (component.tags && component.tags.length > 0) {
      content += `## Tags\n\n`;
      content += component.tags.map((tag) => `\`${tag}\``).join(', ');
      content += '\n';
    }

    return content;
  }

  private _getHtmlForWebview(webview: vscode.Webview) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Component Knowledge Base</title>
    <style>
        body {
            padding: 10px;
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
        }
        
        h2 {
            font-size: 16px;
            margin-bottom: 10px;
            border-bottom: 1px solid var(--vscode-panel-border);
            padding-bottom: 8px;
        }
        
        .search-box {
            width: 100%;
            padding: 8px;
            margin-bottom: 15px;
            background: var(--vscode-input-background);
            color: var(--vscode-input-foreground);
            border: 1px solid var(--vscode-input-border);
            border-radius: 3px;
            font-family: var(--vscode-font-family);
        }
        
        .actions {
            display: flex;
            gap: 8px;
            margin-bottom: 15px;
        }
        
        button {
            padding: 6px 12px;
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
        }
        
        button:hover {
            background: var(--vscode-button-hoverBackground);
        }
        
        .component-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .component-item {
            padding: 10px;
            background: var(--vscode-list-inactiveSelectionBackground);
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.2s;
        }
        
        .component-item:hover {
            background: var(--vscode-list-hoverBackground);
        }
        
        .component-name {
            font-weight: 600;
            font-size: 14px;
            margin-bottom: 4px;
        }
        
        .component-description {
            font-size: 12px;
            color: var(--vscode-descriptionForeground);
            margin-bottom: 6px;
        }
        
        .component-meta {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .tag {
            font-size: 10px;
            padding: 2px 6px;
            background: var(--vscode-badge-background);
            color: var(--vscode-badge-foreground);
            border-radius: 3px;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: var(--vscode-descriptionForeground);
        }
        
        .empty-state-icon {
            font-size: 48px;
            margin-bottom: 16px;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: var(--vscode-descriptionForeground);
        }
        
        .error {
            padding: 10px;
            background: var(--vscode-inputValidation-errorBackground);
            border: 1px solid var(--vscode-inputValidation-errorBorder);
            border-radius: 3px;
            margin-bottom: 15px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <h2>Component Knowledge Base</h2>
    
    <div class="actions">
        <button onclick="scanFolder()">Scan Folder</button>
        <button onclick="refresh()">Refresh</button>
    </div>
    
    <input 
        type="text" 
        class="search-box" 
        placeholder="Search components..." 
        id="searchInput"
        oninput="search()"
    />
    
    <div id="error" class="error" style="display: none;"></div>
    
    <div id="loading" class="loading" style="display: none;">Loading...</div>
    
    <div id="componentList" class="component-list"></div>
    
    <div id="emptyState" class="empty-state" style="display: none;">
        <div class="empty-state-icon">📦</div>
        <div>No components indexed yet</div>
        <div style="margin-top: 10px; font-size: 12px;">
            Click "Scan Folder" to index your component library
        </div>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        let allComponents = [];
        
        // Request components on load
        window.addEventListener('load', () => {
            showLoading(true);
            vscode.postMessage({ type: 'getComponents' });
        });
        
        // Handle messages from extension
        window.addEventListener('message', event => {
            const message = event.data;
            
            switch (message.type) {
                case 'componentsLoaded':
                    allComponents = message.components;
                    renderComponents(allComponents);
                    showLoading(false);
                    break;
                    
                case 'searchResults':
                    renderComponents(message.results);
                    showLoading(false);
                    break;
                    
                case 'error':
                    showError(message.message);
                    showLoading(false);
                    break;
                    
                case 'componentDeleted':
                    allComponents = allComponents.filter(c => c.id !== message.componentId);
                    renderComponents(allComponents);
                    break;
            }
        });
        
        function renderComponents(components) {
            const listEl = document.getElementById('componentList');
            const emptyStateEl = document.getElementById('emptyState');
            
            if (components.length === 0) {
                listEl.innerHTML = '';
                emptyStateEl.style.display = 'block';
                return;
            }
            
            emptyStateEl.style.display = 'none';
            
            listEl.innerHTML = components.map(component => `
                <div class="component-item" onclick="showComponent(${JSON.stringify(component).replace(/"/g, '&quot;')})">
                    <div class="component-name">${escapeHtml(component.name)}</div>
                    <div class="component-description">${escapeHtml(component.description || '')}</div>
                    <div class="component-meta">
                        ${component.category ? `<span class="tag">${escapeHtml(component.category)}</span>` : ''}
                        ${component.props ? `<span class="tag">${component.props.length} props</span>` : ''}
                        ${component.examples ? `<span class="tag">${component.examples.length} examples</span>` : ''}
                    </div>
                </div>
            `).join('');
        }
        
        function showComponent(component) {
            vscode.postMessage({
                type: 'showComponent',
                component: component
            });
        }
        
        function search() {
            const query = document.getElementById('searchInput').value;
            
            if (!query) {
                renderComponents(allComponents);
                return;
            }
            
            showLoading(true);
            vscode.postMessage({
                type: 'searchComponents',
                query: query
            });
        }
        
        function scanFolder() {
            vscode.postMessage({ type: 'scanFolder' });
        }
        
        function refresh() {
            showLoading(true);
            document.getElementById('searchInput').value = '';
            vscode.postMessage({ type: 'getComponents' });
        }
        
        function showLoading(show) {
            document.getElementById('loading').style.display = show ? 'block' : 'none';
        }
        
        function showError(message) {
            const errorEl = document.getElementById('error');
            errorEl.textContent = message;
            errorEl.style.display = 'block';
            setTimeout(() => {
                errorEl.style.display = 'none';
            }, 5000);
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>`;
  }
}

