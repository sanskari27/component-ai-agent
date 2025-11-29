import * as vscode from 'vscode';
import { getRAGClient } from '../rag-client/client';
import { allTools, CopilotTool } from './tools';

export class CopilotAgent {
  private participant: vscode.ChatParticipant | null = null;

  constructor(private context: vscode.ExtensionContext) {}

  /**
   * Register the Copilot chat participant
   */
  register(): void {
    // Register chat participant
    this.participant = vscode.chat.createChatParticipant('component-ai.agent', async (request, context, stream, token) => {
      return this.handleRequest(request, context, stream, token);
    });

    // Set participant properties
    this.participant.iconPath = vscode.Uri.joinPath(
      this.context.extensionUri,
      'resources',
      'icon.png'
    );

    this.context.subscriptions.push(this.participant);

    // Register tools/commands
    for (const tool of allTools) {
      this.registerTool(tool);
    }
  }

  /**
   * Handle Copilot requests
   */
  private async handleRequest(
    request: vscode.ChatRequest,
    context: vscode.ChatContext,
    stream: vscode.ChatResponseStream,
    token: vscode.CancellationToken
  ): Promise<vscode.ChatResult> {
    try {
      // Check if RAG service is available
      const client = getRAGClient();
      const isHealthy = await client.healthCheck();

      if (!isHealthy) {
        stream.markdown(
          '⚠️ RAG service is not running. Please start it using the command: **Component AI: Start RAG Service**'
        );
        return { metadata: { command: '' } };
      }

      // Parse the request
      const query = request.prompt;

      // Determine intent and route to appropriate tool
      const intent = this.determineIntent(query);

      stream.markdown(`🔍 Searching for components...\n\n`);

      if (intent === 'search') {
        return await this.handleSearch(query, stream, token);
      } else if (intent === 'suggest') {
        return await this.handleSuggest(query, stream, token);
      } else if (intent === 'explain') {
        return await this.handleExplain(query, stream, token);
      } else {
        return await this.handleSearch(query, stream, token);
      }
    } catch (error) {
      stream.markdown(`❌ Error: ${error}`);
      return { metadata: { command: '' } };
    }
  }

  /**
   * Determine user intent from query
   */
  private determineIntent(query: string): 'search' | 'suggest' | 'explain' {
    const lowerQuery = query.toLowerCase();

    if (
      lowerQuery.includes('explain') ||
      lowerQuery.includes('what is') ||
      lowerQuery.includes('tell me about')
    ) {
      return 'explain';
    } else if (
      lowerQuery.includes('suggest') ||
      lowerQuery.includes('recommend') ||
      lowerQuery.includes('i need') ||
      lowerQuery.includes('i want to build') ||
      lowerQuery.includes('help me build')
    ) {
      return 'suggest';
    } else {
      return 'search';
    }
  }

  /**
   * Handle search requests
   */
  private async handleSearch(
    query: string,
    stream: vscode.ChatResponseStream,
    token: vscode.CancellationToken
  ): Promise<vscode.ChatResult> {
    const client = getRAGClient();

    try {
      const result = await client.searchComponents({ query, limit: 5 });

      if (result.results.length === 0) {
        stream.markdown('No components found matching your query.');
        return { metadata: { command: '' } };
      }

      stream.markdown(`Found ${result.results.length} components:\n\n`);

      for (const item of result.results) {
        const comp = item.component;
        stream.markdown(`### ${comp.name}\n\n`);
        stream.markdown(`${comp.description}\n\n`);

        if (comp.import_path) {
          stream.markdown(`**Import:** \`import { ${comp.name} } from '${comp.import_path}';\`\n\n`);
        }

        if (comp.props && comp.props.length > 0) {
          stream.markdown(`**Props:**\n`);
          for (const prop of comp.props.slice(0, 3)) {
            stream.markdown(`- \`${prop.name}\`: ${prop.type}${prop.required ? ' (required)' : ''}\n`);
          }
          stream.markdown('\n');
        }

        if (comp.examples && comp.examples.length > 0) {
          const example = comp.examples[0];
          stream.markdown(`**Example:**\n\`\`\`tsx\n${example.code}\n\`\`\`\n\n`);
        }

        stream.markdown(`---\n\n`);
      }

      return { metadata: { command: '' } };
    } catch (error) {
      stream.markdown(`Failed to search: ${error}`);
      return { metadata: { command: '' } };
    }
  }

  /**
   * Handle suggest requests
   */
  private async handleSuggest(
    query: string,
    stream: vscode.ChatResponseStream,
    token: vscode.CancellationToken
  ): Promise<vscode.ChatResult> {
    const client = getRAGClient();

    try {
      const result = await client.suggestComponents(query, 5);

      if (result.results.length === 0) {
        stream.markdown('No component suggestions found for your description.');
        return { metadata: { command: '' } };
      }

      stream.markdown(`Here are ${result.results.length} component suggestions:\n\n`);

      for (const item of result.results) {
        const comp = item.component;
        stream.markdown(`### ${comp.name}\n\n`);
        stream.markdown(`${comp.description}\n\n`);

        if (comp.import_path) {
          stream.markdown(`**Import:** \`import { ${comp.name} } from '${comp.import_path}';\`\n\n`);
        }

        if (comp.examples && comp.examples.length > 0) {
          const example = comp.examples[0];
          stream.markdown(`**Example usage:**\n\`\`\`tsx\n${example.code}\n\`\`\`\n\n`);
        }

        stream.markdown(`---\n\n`);
      }

      return { metadata: { command: '' } };
    } catch (error) {
      stream.markdown(`Failed to get suggestions: ${error}`);
      return { metadata: { command: '' } };
    }
  }

  /**
   * Handle explain requests
   */
  private async handleExplain(
    query: string,
    stream: vscode.ChatResponseStream,
    token: vscode.CancellationToken
  ): Promise<vscode.ChatResult> {
    const client = getRAGClient();

    try {
      // Extract component name from query
      const componentName = this.extractComponentName(query);

      if (!componentName) {
        stream.markdown('Could not determine which component to explain. Please specify a component name.');
        return { metadata: { command: '' } };
      }

      const components = await client.getComponentsByName(componentName);

      if (components.length === 0) {
        stream.markdown(`Component "${componentName}" not found in the knowledge base.`);
        return { metadata: { command: '' } };
      }

      const comp = components[0];

      stream.markdown(`# ${comp.name}\n\n`);
      stream.markdown(`${comp.description}\n\n`);

      if (comp.category) {
        stream.markdown(`**Category:** ${comp.category}\n\n`);
      }

      if (comp.import_path) {
        stream.markdown(`**Import:**\n\`\`\`tsx\nimport { ${comp.name} } from '${comp.import_path}';\n\`\`\`\n\n`);
      }

      if (comp.props && comp.props.length > 0) {
        stream.markdown(`## Props\n\n`);
        for (const prop of comp.props) {
          stream.markdown(`- **${prop.name}**: \`${prop.type}\`${prop.required ? ' (required)' : ' (optional)'}\n`);
          if (prop.description) {
            stream.markdown(`  - ${prop.description}\n`);
          }
        }
        stream.markdown('\n');
      }

      if (comp.examples && comp.examples.length > 0) {
        stream.markdown(`## Examples\n\n`);
        for (const example of comp.examples) {
          stream.markdown(`### ${example.title}\n\n`);
          if (example.description) {
            stream.markdown(`${example.description}\n\n`);
          }
          stream.markdown(`\`\`\`tsx\n${example.code}\n\`\`\`\n\n`);
        }
      }

      return { metadata: { command: '' } };
    } catch (error) {
      stream.markdown(`Failed to explain component: ${error}`);
      return { metadata: { command: '' } };
    }
  }

  /**
   * Extract component name from query
   */
  private extractComponentName(query: string): string | null {
    // Simple extraction - look for capitalized word after "explain", "what is", etc.
    const patterns = [
      /explain\s+(\w+)/i,
      /what\s+is\s+(\w+)/i,
      /tell\s+me\s+about\s+(\w+)/i,
      /(\w+)\s+component/i,
    ];

    for (const pattern of patterns) {
      const match = query.match(pattern);
      if (match && match[1]) {
        return match[1];
      }
    }

    return null;
  }

  /**
   * Register a tool with the participant
   */
  private registerTool(tool: CopilotTool): void {
    // Tools are handled internally in the request handler
    // This is a placeholder for future extensibility
  }
}

