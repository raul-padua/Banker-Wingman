# 🏦💼 The Busy Banker's Wingman

*Because even the busiest bankers need a smart AI sidekick!*

![Demo](https://img.shields.io/badge/Status-Production%20Ready-brightgreen) ![Tech](https://img.shields.io/badge/Tech-RAG%20%2B%20AI-blue) ![Vibes](https://img.shields.io/badge/Vibes-Immaculate-purple)

## 🚀 What This Beast Does

Ever wished you had a genius AI assistant that could:
- 📄 **Digest your financial documents** like a speed-reading accountant
- 💡 **Answer complex queries** with surgical precision
- 🧠 **Think step-by-step** through problems (Chain of Thought reasoning)
- 💬 **Chat naturally** about your data like your smartest colleague

Well, congratulations! You found it. This RAG (Retrieval-Augmented Generation) application is your new financial copilot.

## ⚡ Features That'll Blow Your Mind

- 🎯 **Smart Document Upload**: Drop a PDF, watch the magic happen
- 🔍 **Semantic Search**: Find exactly what you need, even if you can't remember the exact words
- 🤖 **AI-Powered Chat**: Have conversations with your documents (yes, really!)
- 🧮 **Chain of Thought**: Watch the AI think through complex calculations step-by-step
- 🔄 **Persistent State**: Your data sticks around as you navigate between tabs
- 🗑️ **Clean Slate**: Delete everything with one click when you're done

## 🏗️ Architecture (The Cool Stuff Under the Hood)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js UI    │───▶│  FastAPI Beast  │───▶│  OpenAI Brain   │
│   (Vercel)      │    │   (Railway)     │    │   (GPT-4o)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       
         │              ┌─────────────────┐              
         └─────────────▶│ Vector Database │              
                        │  (In-Memory)    │              
                        └─────────────────┘              
```

**Frontend (Next.js)**: Sleek, responsive UI that doesn't suck  
**Backend (FastAPI)**: Lightning-fast Python API with all the AI smarts  
**Vector Store**: Custom in-memory vector database for semantic search  
**AI Integration**: OpenAI's latest models for that premium intelligence  

## 🎮 Quick Start (Get This Running in Minutes)

### Prerequisites
- Node.js 18+ (because we're not living in 2019)
- Python 3.11+ (the sweet spot)
- An OpenAI API key (your golden ticket)

### Local Development
```bash
# Clone this bad boy
git clone https://github.com/raul-padua/Banker-Wingman.git
cd Banker-Wingman

# Fire up the backend
cd api
pip install -r requirements.txt
python app.py

# In another terminal, wake up the frontend
cd ../frontend
npm install
npm run dev
```

Visit `http://localhost:3000` and prepare to be amazed! 🎉

## 🚀 Production Deployment (The Real Deal)

We use a split deployment strategy because we're smart like that:

### Backend → Railway (Container Magic)
1. Fork this repo
2. Sign up at [Railway](https://railway.app) 
3. Connect your GitHub repo
4. Railway auto-detects everything and deploys 🎯
5. Copy your Railway URL

### Frontend → Vercel (Static Site Supremacy)
1. Update `vercel.json` with your Railway URL
2. Connect repo to [Vercel](https://vercel.com)
3. Add `NEXT_PUBLIC_API_URL` environment variable
4. Deploy and watch it fly! 🛸

*Full deployment guide in [DEPLOYMENT.md](./DEPLOYMENT.md)*

## 💻 Tech Stack (The Dream Team)

**Frontend Powerhouse:**
- ⚛️ Next.js 15 - React framework that doesn't hate you
- 🎨 Tailwind CSS - Styling that sparks joy
- 🏛️ Heroicons - Icons that look professional
- 📝 React Markdown - Beautiful text rendering

**Backend Brilliance:**
- ⚡ FastAPI - Python web framework that's actually fast
- 🧠 LlamaIndex - RAG framework for the modern age
- 🔢 Custom Vector Store - In-memory similarity search
- 🤖 OpenAI Integration - The AI that dreams of electric sheep

**Deployment Dynamite:**
- 🚀 Railway - Container hosting that just works
- ⚡ Vercel - Frontend hosting at light speed
- 🐳 Docker - Containerization without the headaches

## 🎯 Core Features Deep Dive

### Document Processing
Upload a PDF and watch our document processor:
- Split text into smart chunks (1024 chars with overlap)
- Generate embeddings using OpenAI's latest models
- Store everything in our custom vector database

### Semantic Search
Ask questions in plain English:
- "What were the Q3 revenue numbers?"
- "Show me compliance issues from last month"
- "Any red flags in the risk assessment?"

### AI Chat with RAG
Get contextual answers that reference your uploaded documents:
- Chain of Thought reasoning for complex problems
- Source citations so you know where answers come from
- Streaming responses for that real-time feel

## 🛠️ Development Commands

```bash
# Backend commands
cd api
python app.py              # Run the API server
pytest                     # Run tests (when we write them)

# Frontend commands  
cd frontend
npm run dev                # Development server
npm run build              # Production build
npm run lint               # Check for code sins
```

## 🔧 Environment Variables

### Backend (Optional)
```bash
PORT=8000                  # Server port (Railway sets this)
OPENAI_API_KEY=sk-...     # Optional fallback (users provide their own)
```

### Frontend
```bash
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

## 🎨 File Structure (For the Organized Minds)

```
📦 Banker-Wingman
├── 📁 api/                    # Backend FastAPI goodness
│   ├── 📁 utils/              # Helper modules
│   ├── 📄 app.py              # Main API application
│   └── 📄 requirements.txt    # Python dependencies
├── 📁 frontend/               # Next.js frontend magic
│   ├── 📁 src/                # Source code
│   ├── 📁 public/             # Static assets
│   └── 📄 package.json        # Node dependencies
├── 📄 Dockerfile             # Container configuration
├── 📄 railway.json           # Railway deployment config
├── 📄 vercel.json            # Vercel configuration
└── 📄 DEPLOYMENT.md          # Deployment instructions
```

## 🐛 Common Issues & Solutions

**"API not connecting"** → Check your `NEXT_PUBLIC_API_URL` environment variable

**"No documents found"** → Make sure you uploaded a PDF first!

**"OpenAI API errors"** → Double-check your API key and billing

**"Port already in use"** → Kill that rogue process: `lsof -ti:8000 | xargs kill`

## 🤝 Contributing (Join the Fun!)

Got ideas? Found bugs? Want to make this even more awesome?

1. Fork the repo
2. Create a feature branch
3. Make your magic happen
4. Open a PR with a killer description

## 📜 License

MIT License - Go wild, build amazing things! 🎉

## 🙏 Acknowledgments

- OpenAI for the brain power 🧠
- LlamaIndex for RAG magic 🦙
- The Next.js team for making React fun again ⚛️
- Railway for deployment that doesn't suck 🚂

---

*Built with ❤️ and way too much coffee by developers who believe banking tech shouldn't be boring*

**Star this repo if it made your day! ⭐**
