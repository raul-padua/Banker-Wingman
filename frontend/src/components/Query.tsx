import { useState, useEffect } from 'react';
// import { QueryResult } from '@/types'; // Unused import
import { queryDocuments } from '@/lib/api';
import ReactMarkdown from 'react-markdown';
import { useAppContext } from '@/contexts/AppContext';

export default function Query() {
  const [currentQueryInput, setCurrentQueryInput] = useState('');

  const {
    lastQuery,
    setLastQuery,
    queryResults,
    setQueryResults,
    isQueryLoading,
    setIsQueryLoading,
    queryError,
    setQueryError
  } = useAppContext();

  useEffect(() => {
    if (lastQuery) {
      setCurrentQueryInput(lastQuery);
    }
  }, [lastQuery]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentQueryInput.trim() || isQueryLoading) return;

    const apiKey = localStorage.getItem('apiKey');
    if (!apiKey) {
      setQueryError('Please enter your OpenAI API key in the field above to use the query feature.');
      setQueryResults([]);
      return;
    }

    setIsQueryLoading(true);
    setQueryError(null);

    try {
      const response = await queryDocuments({
        query: currentQueryInput.trim(),
        limit: 5,
        score_threshold: 0.7
      });

      if (response.error) {
        if (response.error.includes('API key')) {
          setQueryError('Invalid API key. Please check your API key and try again.');
        } else {
          setQueryError(response.error || 'An unknown error occurred during query.');
        }
        setQueryResults([]);
        return;
      }

      if (response.data) {
        console.log("Frontend: Setting query results:", response.data.results);
        setQueryResults(response.data.results || []);
        setLastQuery(currentQueryInput.trim());
        setQueryError(null);
      }
    } catch (err: unknown) {
      if (err instanceof Error) {
        setQueryError(err.message || 'Failed to query documents');
      } else {
        setQueryError('An unknown error occurred while querying documents');
      }
      setQueryResults([]);
    } finally {
      setIsQueryLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <form onSubmit={handleSubmit} className="mb-6">
        <div className="flex space-x-4">
          <input
            type="text"
            value={currentQueryInput}
            onChange={(e) => setCurrentQueryInput(e.target.value)}
            placeholder="Ask a question about your documents..."
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isQueryLoading}
          />
          <button
            type="submit"
            disabled={isQueryLoading || !currentQueryInput.trim()}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isQueryLoading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      {queryError && (
        <div className="p-4 mb-4 text-red-700 bg-red-100 rounded-lg">
          {queryError}
        </div>
      )}

      <div className="space-y-4">
        {queryResults.map((result, index) => (
          <div
            key={`${result.metadata.file_name}-${result.metadata.page_number}-${result.score}-${index}`}
            className="p-4 border rounded-lg bg-white shadow-sm"
          >
            <div className="flex justify-between items-start mb-2">
              <div className="text-sm text-gray-500">
                From: {result.metadata.file_name} (Page {result.metadata.page_number})
              </div>
              <div className="text-sm text-gray-500">
                Score: {(result.score * 100).toFixed(1)}%
              </div>
            </div>
            <div className="prose prose-sm max-w-none">
              <ReactMarkdown>{result.text}</ReactMarkdown>
            </div>
            {result.metadata.has_tables && (
              <div className="mt-2 text-sm text-blue-600">
                Contains tables
              </div>
            )}
            {result.metadata.has_images && (
              <div className="mt-2 text-sm text-blue-600">
                Contains images
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
} 