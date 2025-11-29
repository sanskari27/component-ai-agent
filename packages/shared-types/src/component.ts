/**
 * Component metadata and information
 */
export interface Component {
  id: string;
  name: string;
  description: string;
  filePath: string;
  props: ComponentProp[];
  examples: ComponentExample[];
  themeWrapper?: string;
  category?: string;
  tags?: string[];
  importPath?: string;
  exportType?: 'default' | 'named';
  createdAt?: string;
  updatedAt?: string;
}

/**
 * Component prop definition
 */
export interface ComponentProp {
  name: string;
  type: string;
  required: boolean;
  defaultValue?: string;
  description?: string;
}

/**
 * Component usage example
 */
export interface ComponentExample {
  title: string;
  code: string;
  description?: string;
  source?: 'storybook' | 'manual' | 'monorepo';
}

/**
 * Usage pattern from monorepo analysis
 */
export interface UsagePattern {
  componentId: string;
  componentName: string;
  importPath: string;
  propsUsage: Record<string, number>;
  commonPatterns: string[];
  themeWrapperUsage?: string;
  occurrences: number;
}

/**
 * Component metadata extracted from AST
 */
export interface ComponentMetadata {
  name: string;
  filePath: string;
  exportType: 'default' | 'named';
  props: ComponentProp[];
  dependencies: string[];
  hasChildren: boolean;
  isHOC: boolean;
}

/**
 * Storybook story information
 */
export interface StoryInfo {
  title: string;
  componentName: string;
  stories: {
    name: string;
    code: string;
    args?: Record<string, any>;
  }[];
  filePath: string;
}

