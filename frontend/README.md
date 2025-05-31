# RAG Chat Frontend

A modern Next.js frontend for the RAG (Retrieval-Augmented Generation) system. This application provides a user-friendly interface for uploading PDF documents, querying them, and chatting with an AI assistant.

## Features

- PDF document upload with drag-and-drop support
- Document querying with semantic search
- Real-time chat interface with streaming responses
- API key management
- Health monitoring
- Responsive design
- Markdown support in chat and query results

## Prerequisites

- Node.js 18+ and npm
- Backend API running (see backend README)
- OpenAI API key

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env.local` file in the root directory:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Usage

1. **API Key Setup**
   - Enter your OpenAI API key on the welcome screen
   - The key is stored in localStorage for convenience
   - You can change the API key at any time using the button in the header

2. **Upload Documents**
   - Click the "Upload" tab
   - Drag and drop PDF files or click to select
   - Wait for the upload and processing to complete

3. **Query Documents**
   - Click the "Query" tab
   - Enter your question in the search box
   - View results with relevance scores and metadata

4. **Chat**
   - Click the "Chat" tab
   - Type your message and press Enter or click the send button
   - View streaming responses in real-time

## Development

- Built with Next.js 14
- Uses TypeScript for type safety
- Styled with Tailwind CSS
- Uses Headless UI for accessible components
- Implements responsive design for all screen sizes

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js app directory
│   ├── components/       # React components
│   ├── lib/             # Utility functions and API client
│   └── types/           # TypeScript type definitions
├── public/              # Static assets
└── package.json         # Dependencies and scripts
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking
