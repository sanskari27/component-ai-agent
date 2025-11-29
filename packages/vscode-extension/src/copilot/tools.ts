import * as vscode from 'vscode';
import { getRAGClient } from '../rag-client/client';

export interface CopilotTool {
  name: string;
  description: string;
  parametersSchema: any;
  handler: (parameters: any, token: vscode.CancellationToken) => Promise<any>;
}

/**
 * Search for components using semantic search
 */
export const searchComponentsTool: CopilotTool = {
  name: 'searchComponents',
  description:
    'Search for React components using semantic search. Use this when the user asks about finding components or needs component suggestions.',
  parametersSchema: {
    type: 'object',
    properties: {
      query: {
        type: 'string',
        description: 'Search query describing the component to find',
      },
      limit: {
        type: 'number',
        description: 'Maximum number of results to return',
        default: 10,
      },
    },
    required: ['query'],
  },
  handler: async (parameters: any, token: vscode.CancellationToken) => {
    const client = getRAGClient();
    try {
      const result = await client.searchComponents({
        query: parameters.query,
        limit: parameters.limit || 10,
      });

      return {
        success: true,
        components: result.results.map((r) => ({
          name: r.component.name,
          description: r.component.description,
          importPath: r.component.import_path,
          props: r.component.props,
          score: r.score,
        })),
      };
    } catch (error) {
      return {
        success: false,
        error: `Failed to search components: ${error}`,
      };
    }
  },
};

/**
 * Get detailed information about a specific component
 */
export const explainComponentTool: CopilotTool = {
  name: 'explainComponent',
  description:
    'Get detailed information about a specific component including props, examples, and usage patterns.',
  parametersSchema: {
    type: 'object',
    properties: {
      componentName: {
        type: 'string',
        description: 'Name of the component to explain',
      },
    },
    required: ['componentName'],
  },
  handler: async (parameters: any, token: vscode.CancellationToken) => {
    const client = getRAGClient();
    try {
      const components = await client.getComponentsByName(parameters.componentName);

      if (components.length === 0) {
        return {
          success: false,
          error: `Component "${parameters.componentName}" not found`,
        };
      }

      const component = components[0];
      return {
        success: true,
        component: {
          name: component.name,
          description: component.description,
          filePath: component.file_path,
          importPath: component.import_path,
          exportType: component.export_type,
          props: component.props,
          examples: component.examples,
          themeWrapper: component.theme_wrapper,
          category: component.category,
          tags: component.tags,
        },
      };
    } catch (error) {
      return {
        success: false,
        error: `Failed to get component details: ${error}`,
      };
    }
  },
};

/**
 * Suggest components based on UI description
 */
export const suggestComponentForUITool: CopilotTool = {
  name: 'suggestComponentForUI',
  description:
    'Suggest components that match a UI description. Use this when the user describes a UI element they want to build.',
  parametersSchema: {
    type: 'object',
    properties: {
      uiDescription: {
        type: 'string',
        description: 'Description of the UI element or feature',
      },
      limit: {
        type: 'number',
        description: 'Maximum number of suggestions',
        default: 5,
      },
    },
    required: ['uiDescription'],
  },
  handler: async (parameters: any, token: vscode.CancellationToken) => {
    const client = getRAGClient();
    try {
      const result = await client.suggestComponents(
        parameters.uiDescription,
        parameters.limit || 5
      );

      return {
        success: true,
        suggestions: result.results.map((r) => ({
          name: r.component.name,
          description: r.component.description,
          importPath: r.component.import_path,
          props: r.component.props,
          score: r.score,
          examples: r.component.examples.slice(0, 1), // Include first example
        })),
      };
    } catch (error) {
      return {
        success: false,
        error: `Failed to suggest components: ${error}`,
      };
    }
  },
};

/**
 * Scan a component folder and index components
 */
export const scanComponentFolderTool: CopilotTool = {
  name: 'scanComponentFolder',
  description:
    'Scan a folder for React components and add them to the knowledge base. Use this when the user wants to index new components.',
  parametersSchema: {
    type: 'object',
    properties: {
      folderPath: {
        type: 'string',
        description: 'Path to the folder containing components',
      },
      includeStorybooks: {
        type: 'boolean',
        description: 'Whether to include Storybook examples',
        default: true,
      },
      recursive: {
        type: 'boolean',
        description: 'Whether to scan recursively',
        default: true,
      },
    },
    required: ['folderPath'],
  },
  handler: async (parameters: any, token: vscode.CancellationToken) => {
    const client = getRAGClient();
    try {
      const result = await client.scanFolder({
        folder_path: parameters.folderPath,
        include_storybooks: parameters.includeStorybooks !== false,
        include_tests: false,
        recursive: parameters.recursive !== false,
      });

      return {
        success: true,
        componentsFound: result.components_found,
        components: result.components.map((c) => c.name),
        errors: result.errors,
      };
    } catch (error) {
      return {
        success: false,
        error: `Failed to scan folder: ${error}`,
      };
    }
  },
};

export const allTools: CopilotTool[] = [
  searchComponentsTool,
  explainComponentTool,
  suggestComponentForUITool,
  scanComponentFolderTool,
];

