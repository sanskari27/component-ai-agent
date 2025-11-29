# Shared Types

TypeScript type definitions shared between the VS Code extension and other packages.

## Structure

- `component.ts` - Component metadata, props, examples, and usage patterns
- `rag.ts` - RAG service request/response types
- `index.ts` - Main entry point

## Usage

```typescript
import { Component, SearchRequest, SearchResponse } from '@component-ai/shared-types';
```

## Building

```bash
pnpm build
```

