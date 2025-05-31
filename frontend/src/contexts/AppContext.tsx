import React, { createContext, useState, useContext, ReactNode } from 'react';
import { QueryResult, ChatMessage } from '@/types'; // Assuming your types are in @/types

// Define the shape of the context data
interface AppContextType {
  // Uploaded file state
  uploadedFileName: string | null;
  setUploadedFileName: (name: string | null) => void;
  isUploading: boolean;
  setIsUploading: (status: boolean) => void;
  uploadError: string | null;
  setUploadError: (error: string | null) => void;
  uploadSuccessMessage: string | null;
  setUploadSuccessMessage: (message: string | null) => void;


  // Query results state
  lastQuery: string | null;
  setLastQuery: (query: string | null) => void;
  queryResults: QueryResult[];
  setQueryResults: (results: QueryResult[]) => void;
  isQueryLoading: boolean;
  setIsQueryLoading: (status: boolean) => void;
  queryError: string | null;
  setQueryError: (error: string | null) => void;

  // Chat messages state
  chatMessages: ChatMessage[];
  setChatMessages: React.Dispatch<React.SetStateAction<ChatMessage[]>>;
  isChatLoading: boolean;
  setIsChatLoading: (status: boolean) => void;
  // We might not need a separate chatError in context if components handle their own transient errors
}

// Create the context with a default undefined value
const AppContext = createContext<AppContextType | undefined>(undefined);

// Create a provider component
interface AppProviderProps {
  children: ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  // Uploaded file state
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [uploadSuccessMessage, setUploadSuccessMessage] = useState<string | null>(null);

  // Query results state
  const [lastQuery, setLastQuery] = useState<string | null>(null);
  const [queryResults, setQueryResults] = useState<QueryResult[]>([]);
  const [isQueryLoading, setIsQueryLoading] = useState<boolean>(false);
  const [queryError, setQueryError] = useState<string | null>(null);
  
  // Chat messages state
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [isChatLoading, setIsChatLoading] = useState<boolean>(false);

  const contextValue: AppContextType = {
    uploadedFileName,
    setUploadedFileName,
    isUploading,
    setIsUploading,
    uploadError,
    setUploadError,
    uploadSuccessMessage,
    setUploadSuccessMessage,
    lastQuery,
    setLastQuery,
    queryResults,
    setQueryResults,
    isQueryLoading,
    setIsQueryLoading,
    queryError,
    setQueryError,
    chatMessages,
    setChatMessages,
    isChatLoading,
    setIsChatLoading,
  };

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  );
};

// Create a custom hook to use the AppContext
export const useAppContext = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
}; 