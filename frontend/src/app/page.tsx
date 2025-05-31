'use client';

import { useState, useEffect, useCallback } from 'react';
import { Tab } from '@headlessui/react';
import FileUpload from '@/components/FileUpload';
import Chat from '@/components/Chat';
import Query from '@/components/Query';
import { checkHealth, deleteDocuments } from '@/lib/api';
import { AppProvider, useAppContext } from '@/contexts/AppContext';
import { DocumentCheckIcon, TrashIcon } from '@heroicons/react/24/solid';

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ');
}

function PageContent() {
  const {
    uploadedFileName,
    setUploadedFileName,
    setUploadError,
    setUploadSuccessMessage,
    setLastQuery,
    setQueryResults,
    setQueryError,
    setChatMessages,
    uploadError
  } = useAppContext();

  const [isDeleting, setIsDeleting] = useState(false);
  const [deleteError, setDeleteError] = useState<string | null>(null);

  const handleDeleteDocument = async () => {
    const apiKey = localStorage.getItem('apiKey');
    if (!apiKey) {
      setDeleteError("API Key not found. Please ensure it's set.");
      return;
    }
    if (!uploadedFileName) {
        setDeleteError("No document is currently registered as uploaded.");
        return;
    }

    const confirmDelete = window.confirm(
      `Are you sure you want to delete the uploaded document '${uploadedFileName}' and all associated data (queries, chat history)? This action cannot be undone.`
    );

    if (!confirmDelete) {
      return;
    }

    setIsDeleting(true);
    setDeleteError(null);

    try {
      const response = await deleteDocuments();
      if (response.error) {
        setDeleteError(response.error);
      } else {
        setUploadedFileName(null);
        setUploadError(null);
        setUploadSuccessMessage('Document and associated data deleted successfully.');
        setLastQuery(null);
        setQueryResults([]);
        setQueryError(null);
        setChatMessages([]);
      }
    } catch (err: unknown) {
      if (err instanceof Error) {
        setDeleteError(err.message || 'Failed to delete document');
      } else {
        setDeleteError('An unknown error occurred while deleting the document');
      }
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <>
      {uploadedFileName && !uploadError && (
        <div className="my-4 flex justify-end items-center">
          <span className="text-sm text-green-700 mr-2">
            Active document: {uploadedFileName}
          </span>
          <button
            onClick={handleDeleteDocument}
            disabled={isDeleting}
            className="px-3 py-1.5 text-xs font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
          >
            <TrashIcon className="inline-block w-4 h-4 mr-1" />
            {isDeleting ? 'Deleting...' : 'Delete Document & Data'}
          </button>
        </div>
      )}
      {deleteError && (
          <div className="my-2 p-3 text-sm text-red-700 bg-red-100 rounded-lg">
              Deletion Error: {deleteError}
          </div>
      )}
      <Tab.Group>
        <Tab.List className="flex space-x-1 rounded-xl bg-blue-900/20 p-1">
          <Tab
            className={({ selected }) =>
              classNames(
                'w-full rounded-lg py-2.5 text-sm font-medium leading-5',
                'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2',
                selected
                  ? 'bg-white text-blue-700 shadow'
                  : 'text-blue-100 hover:bg-white/[0.12] hover:text-white'
              )
            }
          >
            Upload
            {uploadedFileName && !uploadError && (
              <DocumentCheckIcon className="inline-block w-5 h-5 ml-2 text-green-500" />
            )}
          </Tab>
          <Tab
            className={({ selected }) =>
              classNames(
                'w-full rounded-lg py-2.5 text-sm font-medium leading-5',
                'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2',
                selected
                  ? 'bg-white text-blue-700 shadow'
                  : 'text-blue-100 hover:bg-white/[0.12] hover:text-white'
              )
            }
          >
            Query
          </Tab>
          <Tab
            className={({ selected }) =>
              classNames(
                'w-full rounded-lg py-2.5 text-sm font-medium leading-5',
                'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2',
                selected
                  ? 'bg-white text-blue-700 shadow'
                  : 'text-blue-100 hover:bg-white/[0.12] hover:text-white'
              )
            }
          >
            Chat
          </Tab>
        </Tab.List>
        <Tab.Panels className="mt-6">
          <Tab.Panel>
            <FileUpload />
          </Tab.Panel>
          <Tab.Panel>
            <Query />
          </Tab.Panel>
          <Tab.Panel>
            <Chat />
          </Tab.Panel>
        </Tab.Panels>
      </Tab.Group>
    </>
  );
}

export default function Home() {
  const [apiKey, setApiKey] = useState('');
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);

  useEffect(() => {
    const storedApiKey = localStorage.getItem('apiKey');
    if (storedApiKey) {
      setApiKey(storedApiKey);
    }
  }, []);

  useEffect(() => {
    const checkApiHealth = async () => {
      try {
        const response = await checkHealth();
        setIsHealthy(response.data?.status === 'ok');
      } catch (error) {
        setIsHealthy(false);
      }
    };

    if (apiKey) {
      checkApiHealth();
    }
  }, [apiKey]);

  const handleApiKeySubmit = (e: React.FormEvent) => {
    e.preventDefault();
    localStorage.setItem('apiKey', apiKey);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <AppProvider>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <div className="flex justify-between items-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900">The Busy Banker's Wingman</h1>
              <div className="flex items-center space-x-4">
                <form onSubmit={handleApiKeySubmit} className="flex items-center space-x-2">
                  <input
                    type="password"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    className="appearance-none rounded-lg relative block px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                    placeholder="OpenAI API Key"
                  />
                  <button
                    type="submit"
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    Save Key
                  </button>
                </form>
                <div
                  className={`flex items-center ${
                    isHealthy ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  <div
                    className={`w-3 h-3 rounded-full mr-2 ${
                      isHealthy ? 'bg-green-500' : 'bg-red-500'
                    }`}
                  />
                  <span className="text-sm">
                    {isHealthy ? 'API Connected' : 'API Disconnected'}
                  </span>
                </div>
              </div>
            </div>
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg text-blue-700 text-sm">
              <h2 className="text-lg font-semibold mb-2">Welcome to your AI-powered financial assistant</h2>
              <p>
                Upload your financial documents, ask questions, and get insights with the help of advanced AI. 
                Use the Query tab for specific data retrieval from your documents and the Chat tab for conversational analysis, 
                reasoning, and a summary of your findings.
              </p>
            </div>
            <PageContent />
          </div>
        </div>
      </AppProvider>
    </div>
  );
}
