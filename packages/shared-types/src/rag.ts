/**
 * Search request for semantic component search
 */
export interface SearchRequest {
  query: string;
  limit?: number;
  filters?: SearchFilters;
}

/**
 * Search filters
 */
export interface SearchFilters {
  category?: string;
  tags?: string[];
  hasProps?: string[];
}

/**
 * Search result item
 */
export interface SearchResult {
  component: Component;
  score: number;
  matchedFields: string[];
}

/**
 * Search response
 */
export interface SearchResponse {
  results: SearchResult[];
  total: number;
  query: string;
}

/**
 * Component explanation request
 */
export interface ExplainComponentRequest {
  componentId?: string;
  componentName?: string;
}

/**
 * Component explanation response
 */
export interface ExplainComponentResponse {
  component: Component;
  usagePatterns?: UsagePattern[];
  relatedComponents?: Component[];
}

/**
 * Suggest component for UI request
 */
export interface SuggestComponentRequest {
  uiDescription: string;
  context?: string;
  limit?: number;
}

/**
 * Scan component folder request
 */
export interface ScanComponentFolderRequest {
  folderPath: string;
  includeStorybooks?: boolean;
  includeTests?: boolean;
  recursive?: boolean;
}

/**
 * Scan result
 */
export interface ScanResult {
  componentsFound: number;
  components: Component[];
  errors?: string[];
}

/**
 * RAG pipeline request
 */
export interface RAGRequest {
  query: string;
  context?: string;
  maxResults?: number;
}

/**
 * RAG pipeline response
 */
export interface RAGResponse {
  results: SearchResult[];
  generatedText?: string;
  metadata?: Record<string, any>;
}

import { Component, UsagePattern } from './component';

