export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface QueryResult {
  text: string;
  metadata: {
    file_name: string;
    page_number: number;
    has_tables: boolean;
    has_images: boolean;
  };
  score: number;
}

export interface ApiQueryResponse {
  results: QueryResult[];
  query: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
}

export interface UploadResponse {
  message: string;
  chunks: number;
  filename: string;
}

export interface QueryRequest {
  query: string;
  limit?: number;
  score_threshold?: number;
}

export interface ChatRequest {
  developer_message: string;
  user_message: string;
  model?: string;
} 