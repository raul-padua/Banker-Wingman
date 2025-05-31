import { useState, useRef, useEffect, useCallback } from 'react';
import { ChatMessage } from '@/types';
import { chat } from '../lib/api';
import ReactMarkdown from 'react-markdown';
import { PaperAirplaneIcon } from '@heroicons/react/24/outline';
import { useAppContext } from '@/contexts/AppContext';

export default function Chat() {
  const {
    chatMessages,
    setChatMessages,
    isChatLoading,
    setIsChatLoading
  } = useAppContext();

  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [chatMessages, scrollToBottom]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isChatLoading) return;

    const apiKey = localStorage.getItem('apiKey');
    if (!apiKey) {
      setChatMessages((prevMessages: ChatMessage[]) => [...prevMessages, {
        role: 'assistant',
        content: 'Please enter your OpenAI API key in the field above to use the chat feature.'
      }]);
      return;
    }

    const userMessage: ChatMessage = {
      role: 'user',
      content: input.trim()
    };

    setChatMessages((prevMessages: ChatMessage[]) => [
      ...prevMessages,
      userMessage,
      { role: 'assistant', content: '' }
    ]);
    setInput('');
    setIsChatLoading(true);

    try {
      const response = await chat({
        developer_message: "You are a helpful assistant that answers questions based on the provided context.",
        user_message: userMessage.content
      });

      if (response.error) {
        let errorMessageContent = 'Sorry, I encountered an error. Please try again.';
        if (response.error.includes('API key')) {
          errorMessageContent = 'Invalid API key. Please check your API key and try again.';
        } else if (response.error.includes('HTTP error')) {
          errorMessageContent = response.error;
        } else {
          errorMessageContent = response.error;
        }
        setChatMessages((prevMessages: ChatMessage[]) => prevMessages.map((msg: ChatMessage, index: number) => 
          index === prevMessages.length - 1 ? { ...msg, content: errorMessageContent } : msg
        ));
        return;
      }

      if (response.data) {
        const reader = response.data.getReader();
        let assistantMessageContent = '';
        
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const textChunk = new TextDecoder().decode(value);
          assistantMessageContent += textChunk;
          
          setChatMessages((prevMessages: ChatMessage[]) => prevMessages.map((msg: ChatMessage, index: number) => 
            index === prevMessages.length - 1 ? { ...msg, content: assistantMessageContent } : msg
          ));
        }
      }
    } catch (error: any) {
      setChatMessages((prevMessages: ChatMessage[]) => prevMessages.map((msg: ChatMessage, index: number) => 
        index === prevMessages.length - 1 ? { ...msg, content: 'Sorry, an unexpected error occurred. Please try again.' } : msg
      ));
    } finally {
      setIsChatLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] max-w-2xl mx-auto">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {chatMessages.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-4 ${
                message.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              <ReactMarkdown>
                {message.content}
              </ReactMarkdown>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex space-x-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isChatLoading}
          />
          <button
            type="submit"
            disabled={isChatLoading || !input.trim()}
            className="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <PaperAirplaneIcon className="h-5 w-5" />
          </button>
        </div>
      </form>
    </div>
  );
} 