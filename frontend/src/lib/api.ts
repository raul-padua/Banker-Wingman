import axios, { AxiosError } from 'axios';
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { ApiResponse, ChatRequest, QueryRequest, QueryResult, UploadResponse, ApiQueryResponse } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add API key to all requests
api.interceptors.request.use((config) => {
  const apiKey = localStorage.getItem('apiKey');
  if (apiKey) {
    config.headers['X-API-Key'] = apiKey;
  }
  return config;
});

export const uploadFile = async (file: File): Promise<ApiResponse<UploadResponse>> => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    const apiKey = localStorage.getItem('apiKey');

    console.log('Uploading file with API key:', apiKey);

    const response = await axios.post<UploadResponse>(
      `${API_URL}/api/upload`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          ...(apiKey ? { 'X-API-Key': apiKey } : {}),
        },
        withCredentials: false,
      }
    );

    return { data: response.data };
  } catch (error: unknown) {
    let message = 'Failed to upload file';
    if (axios.isAxiosError(error)) {
      message = error.response?.data?.detail || error.message || message;
    } else if (error instanceof Error) {
      message = error.message;
    }
    return { error: message };
  }
};

export const queryDocuments = async (request: QueryRequest): Promise<ApiResponse<ApiQueryResponse>> => {
  try {
    const response = await api.post<ApiQueryResponse>('/api/query', request);
    return { data: response.data };
  } catch (error: unknown) {
    let message = 'Failed to query documents';
    if (axios.isAxiosError(error)) {
      message = error.response?.data?.detail || error.message || message;
    } else if (error instanceof Error) {
      message = error.message;
    }
    return { error: message };
  }
};

export const chat = async (request: ChatRequest): Promise<ApiResponse<ReadableStream>> => {
  try {
    const apiKey = localStorage.getItem('apiKey');
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };
    if (apiKey) {
      headers['X-API-Key'] = apiKey;
    }

    const response = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers,
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      // Attempt to read error message from response body
      let errorDetail = 'Failed to send chat message';
      try {
        const errorData = await response.json();
        errorDetail = errorData.detail || errorDetail;
      } catch (_e: unknown) {
        // Ignore if response is not JSON or already consumed
      }
      return { error: `HTTP error ${response.status}: ${errorDetail}` };
    }

    if (!response.body) {
      return { error: 'Response body is null' };
    }
    
    return { data: response.body }; // response.body from fetch IS a ReadableStream

  } catch (error: unknown) {
    let message = 'Failed to send chat message';
    if (error instanceof Error) {
        message = error.message;
    }
    return { error: message };
  }
};

export const deleteDocuments = async (): Promise<ApiResponse<{ detail: string }>> => {
  try {
    const apiKey = localStorage.getItem('apiKey');
    const headers: HeadersInit = {
      'Content-Type': 'application/json', // Though not strictly needed for DELETE with no body
    };
    if (apiKey) {
      headers['X-API-Key'] = apiKey;
    }

    const response = await fetch(`${API_URL}/api/documents`, {
      method: 'DELETE',
      headers,
    });

    if (!response.ok) {
      let errorDetail = 'Failed to delete documents';
      try {
        const errorData = await response.json();
        errorDetail = errorData.detail || errorDetail;
      } catch (_e: unknown) {
        // Ignore if response is not JSON or already consumed
      }
      return { error: `HTTP error ${response.status}: ${errorDetail}` };
    }
    // If DELETE is successful, backend returns 200 with a detail message
    const responseData = await response.json(); 
    return { data: responseData }; 

  } catch (error: unknown) {
    let message = 'An unexpected error occurred while deleting documents';
    if (error instanceof Error) {
        message = error.message;
    } 
    return { error: message };
  }
};

export const checkHealth = async (): Promise<ApiResponse<{ status: string }>> => {
  try {
    const response = await api.get<{ status: string }>('/api/health');
    return { data: response.data };
  } catch {
    return { error: 'Service is unhealthy' };
  }
}; 