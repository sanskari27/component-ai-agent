import * as vscode from 'vscode';
import { CopilotAgent } from './copilot/agent';
import { getRAGClient } from './rag-client/client';
import { KnowledgeBaseProvider } from './sidebar/provider';
import { ServiceManager } from './utils/service-manager';

let serviceManager: ServiceManager;
let copilotAgent: CopilotAgent;
let knowledgeBaseProvider: KnowledgeBaseProvider;
let outputChannel: vscode.OutputChannel;

export async function activate(context: vscode.ExtensionContext) {
  console.log('Component AI Agent is now active');

  // Create output channel
  outputChannel = vscode.window.createOutputChannel('Component AI');
  context.subscriptions.push(outputChannel);

  // Initialize service manager
  serviceManager = new ServiceManager(outputChannel);

  // Register Copilot agent
  copilotAgent = new CopilotAgent(context);
  copilotAgent.register();

  // Register sidebar webview
  knowledgeBaseProvider = new KnowledgeBaseProvider(context.extensionUri);
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider('component-ai.knowledgeBase', knowledgeBaseProvider)
  );

  // Register commands
  context.subscriptions.push(
    vscode.commands.registerCommand('component-ai.startService', async () => {
      const config = vscode.workspace.getConfiguration('componentAI');
      const port = config.get<number>('ragService.port', 8765);

      const started = await serviceManager.startService(port);
      if (started) {
        vscode.window.showInformationMessage('RAG service started successfully');
      } else {
        vscode.window.showErrorMessage('Failed to start RAG service');
      }
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('component-ai.stopService', () => {
      serviceManager.stopService();
      vscode.window.showInformationMessage('RAG service stopped');
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('component-ai.scanFolder', async () => {
      const folderUri = await vscode.window.showOpenDialog({
        canSelectFolders: true,
        canSelectFiles: false,
        canSelectMany: false,
        openLabel: 'Select Component Folder',
      });

      if (!folderUri || folderUri.length === 0) {
        return;
      }

      const folderPath = folderUri[0].fsPath;

      try {
        const client = getRAGClient();
        const result = await vscode.window.withProgress(
          {
            location: vscode.ProgressLocation.Notification,
            title: 'Scanning components...',
            cancellable: false,
          },
          async () => {
            return await client.scanFolder({
              folder_path: folderPath,
              include_storybooks: true,
              include_tests: false,
              recursive: true,
            });
          }
        );

        vscode.window.showInformationMessage(`Scanned ${result.components_found} components`);

        // Refresh sidebar
        knowledgeBaseProvider.refresh();
      } catch (error) {
        vscode.window.showErrorMessage(`Failed to scan folder: ${error}`);
      }
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('component-ai.showKnowledgeBase', () => {
      vscode.commands.executeCommand('component-ai.knowledgeBase.focus');
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('component-ai.refreshComponents', () => {
      knowledgeBaseProvider.refresh();
      vscode.window.showInformationMessage('Components refreshed');
    })
  );

  // Auto-start service if configured
  const config = vscode.workspace.getConfiguration('componentAI');
  const autoStart = config.get<boolean>('ragService.autoStart', true);

  if (autoStart) {
    const port = config.get<number>('ragService.port', 8765);
    outputChannel.appendLine('Auto-starting RAG service...');
    await serviceManager.startService(port);
  }

  // Auto-scan configured paths
  const componentPaths = config.get<string[]>('componentAI.componentPaths', []);
  if (componentPaths.length > 0) {
    outputChannel.appendLine('Auto-scanning configured component paths...');
    for (const path of componentPaths) {
      try {
        const client = getRAGClient();
        await client.scanFolder({
          folder_path: path,
          include_storybooks: true,
          include_tests: false,
          recursive: true,
        });
        outputChannel.appendLine(`Scanned: ${path}`);
      } catch (error) {
        outputChannel.appendLine(`Failed to scan ${path}: ${error}`);
      }
    }
  }
}

export function deactivate() {
  if (serviceManager) {
    serviceManager.stopService();
  }
}
