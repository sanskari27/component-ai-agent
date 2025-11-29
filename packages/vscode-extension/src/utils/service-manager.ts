import * as fs from 'fs';
import * as path from 'path';
import * as vscode from 'vscode';

export class ServiceManager {
  private serviceProcess: any = null;
  private outputChannel: vscode.OutputChannel;
  private pythonPath: string = 'python';

  constructor(outputChannel: vscode.OutputChannel) {
    this.outputChannel = outputChannel;
  }

  /**
   * Start the RAG service
   */
  async startService(port: number = 8765): Promise<boolean> {
    if (this.serviceProcess) {
      this.outputChannel.appendLine('RAG service is already running');
      return true;
    }

    try {
      this.outputChannel.appendLine('Starting RAG service...');

      // Find Python path
      const pythonExtension = vscode.extensions.getExtension('ms-python.python');
      if (pythonExtension) {
        if (!pythonExtension.isActive) {
          await pythonExtension.activate();
        }
        const pythonApi = pythonExtension.exports;
        const pythonEnv = await pythonApi.environments.getActiveEnvironmentPath();
        if (pythonEnv) {
          this.pythonPath = pythonEnv.path;
        }
      }

      // Find RAG service path
      const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
      if (!workspaceFolder) {
        throw new Error('No workspace folder found');
      }

      const servicePath = path.join(
        workspaceFolder.uri.fsPath,
        'packages',
        'rag-service',
        'src',
        'main.py'
      );

      if (!fs.existsSync(servicePath)) {
        throw new Error(`RAG service not found at ${servicePath}`);
      }

      // Start the service using spawn
      const { spawn } = require('child_process');
      const serviceDir = path.dirname(path.dirname(servicePath));

      this.serviceProcess = spawn(
        this.pythonPath,
        ['-m', 'uvicorn', 'src.main:app', '--host', '127.0.0.1', '--port', port.toString()],
        {
          cwd: serviceDir,
          env: { ...process.env },
        }
      );

      this.serviceProcess.stdout.on('data', (data: Buffer) => {
        this.outputChannel.appendLine(`[RAG Service] ${data.toString()}`);
      });

      this.serviceProcess.stderr.on('data', (data: Buffer) => {
        this.outputChannel.appendLine(`[RAG Service Error] ${data.toString()}`);
      });

      this.serviceProcess.on('close', (code: number) => {
        this.outputChannel.appendLine(`RAG service exited with code ${code}`);
        this.serviceProcess = null;
      });

      // Wait a bit for the service to start
      await this.waitForService(port);

      this.outputChannel.appendLine('RAG service started successfully');
      return true;
    } catch (error) {
      this.outputChannel.appendLine(`Failed to start RAG service: ${error}`);
      return false;
    }
  }

  /**
   * Stop the RAG service
   */
  stopService(): void {
    if (this.serviceProcess) {
      this.outputChannel.appendLine('Stopping RAG service...');
      this.serviceProcess.kill();
      this.serviceProcess = null;
      this.outputChannel.appendLine('RAG service stopped');
    }
  }

  /**
   * Check if service is running
   */
  isRunning(): boolean {
    return this.serviceProcess !== null;
  }

  /**
   * Wait for the service to be ready
   */
  private async waitForService(port: number, maxAttempts: number = 30): Promise<void> {
    const axios = require('axios');

    for (let i = 0; i < maxAttempts; i++) {
      try {
        await axios.get(`http://localhost:${port}/api/health`, { timeout: 1000 });
        return;
      } catch (error) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
      }
    }

    throw new Error('RAG service failed to start within timeout');
  }
}
