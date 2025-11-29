import {
  Component,
  ScanComponentFolderRequest,
  ScanResult,
  SearchRequest,
  SearchResponse,
} from '@component-ai/shared-types';
import axios, { AxiosInstance } from 'axios';
import * as vscode from 'vscode';

export class RAGClient {
  private client: AxiosInstance;
  private baseUrl: string;

  constructor(port: number = 8765) {
    this.baseUrl = `http://localhost:${port}`;
    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  /**
   * Check if the RAG service is healthy
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.client.get('/api/health');
      return response.data.status === 'healthy';
    } catch (error) {
      return false;
    }
  }

  /**
   * Search for components
   */
  async searchComponents(request: SearchRequest): Promise<SearchResponse> {
    try {
      const response = await this.client.post<SearchResponse>('/api/search', request);
      return response.data;
    } catch (error) {
      console.error('Search failed:', error);
      throw new Error('Failed to search components');
    }
  }

  /**
   * Suggest components based on UI description
   */
  async suggestComponents(query: string, limit: number = 5): Promise<SearchResponse> {
    try {
      const response = await this.client.post<SearchResponse>('/api/search/suggest', {
        query,
        limit,
      });
      return response.data;
    } catch (error) {
      console.error('Suggest failed:', error);
      throw new Error('Failed to suggest components');
    }
  }

  /**
   * Get all components
   */
  async getAllComponents(): Promise<Component[]> {
    try {
      const response = await this.client.get<Component[]>('/api/components');
      return response.data;
    } catch (error) {
      console.error('Failed to get components:', error);
      throw new Error('Failed to get components');
    }
  }

  /**
   * Get component by ID
   */
  async getComponent(componentId: string): Promise<Component> {
    try {
      const response = await this.client.get<Component>(`/api/components/${componentId}`);
      return response.data;
    } catch (error) {
      console.error('Failed to get component:', error);
      throw new Error('Failed to get component');
    }
  }

  /**
   * Get components by name
   */
  async getComponentsByName(name: string): Promise<Component[]> {
    try {
      const response = await this.client.get<Component[]>(`/api/components/name/${name}`);
      return response.data;
    } catch (error) {
      console.error('Failed to get components by name:', error);
      throw new Error('Failed to get components by name');
    }
  }

  /**
   * Create a new component
   */
  async createComponent(component: Component): Promise<Component> {
    try {
      const response = await this.client.post<Component>('/api/components', component);
      return response.data;
    } catch (error) {
      console.error('Failed to create component:', error);
      throw new Error('Failed to create component');
    }
  }

  /**
   * Update a component
   */
  async updateComponent(componentId: string, component: Component): Promise<Component> {
    try {
      const response = await this.client.put<Component>(
        `/api/components/${componentId}`,
        component
      );
      return response.data;
    } catch (error) {
      console.error('Failed to update component:', error);
      throw new Error('Failed to update component');
    }
  }

  /**
   * Delete a component
   */
  async deleteComponent(componentId: string): Promise<void> {
    try {
      await this.client.delete(`/api/components/${componentId}`);
    } catch (error) {
      console.error('Failed to delete component:', error);
      throw new Error('Failed to delete component');
    }
  }

  /**
   * Scan a component folder
   */
  async scanFolder(request: ScanComponentFolderRequest): Promise<ScanResult> {
    try {
      // Convert camelCase to snake_case for Python API
      const pythonRequest = {
        folder_path: request.folderPath,
        include_storybooks: request.includeStorybooks ?? true,
        include_tests: request.includeTests ?? false,
        recursive: request.recursive ?? true,
      };

      const response = await this.client.post('/api/scan', pythonRequest);

      // Convert snake_case response to camelCase
      return {
        componentsFound: response.data.components_found,
        components: response.data.components,
        errors: response.data.errors || [],
      };
    } catch (error) {
      console.error('Scan failed:', error);
      throw new Error('Failed to scan folder');
    }
  }
}

let ragClient: RAGClient | null = null;

export function getRAGClient(): RAGClient {
  if (!ragClient) {
    const config = vscode.workspace.getConfiguration('componentAI');
    const port = config.get<number>('ragService.port', 8765);
    ragClient = new RAGClient(port);
  }
  return ragClient;
}

export function resetRAGClient(): void {
  ragClient = null;
}
