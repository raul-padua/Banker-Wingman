# Deployment Guide

This application uses a split deployment strategy:
- **Frontend**: Deployed on Vercel
- **Backend**: Deployed on Railway (or similar container platform)

## Backend Deployment (Railway)

### Option 1: Railway (Recommended)

1. **Create Railway Account**: Go to [railway.app](https://railway.app) and sign up

2. **Deploy from GitHub**:
   ```bash
   # Connect your GitHub repo to Railway
   # Railway will automatically detect the Dockerfile and railway.json
   ```

3. **Environment Variables**: Set in Railway dashboard:
   ```
   PORT=8000
   OPENAI_API_KEY=your_openai_api_key (optional, users provide their own)
   ```

4. **Deploy**: Railway will build and deploy automatically

5. **Get URL**: Copy your Railway app URL (e.g., `https://your-app.railway.app`)

### Option 2: Render

1. **Create Render Account**: Go to [render.com](https://render.com)

2. **Create Web Service**:
   - Connect GitHub repo
   - Build Command: `pip install -r api/requirements.txt`
   - Start Command: `cd api && uvicorn app:app --host 0.0.0.0 --port $PORT`

### Option 3: Fly.io

1. **Install Fly CLI**: Follow [fly.io docs](https://fly.io/docs/getting-started/installing-flyctl/)

2. **Deploy**:
   ```bash
   fly launch --dockerfile Dockerfile
   fly deploy
   ```

## Frontend Deployment (Vercel)

1. **Update API URL**: Edit `vercel.json` and replace `your-backend-url.railway.app` with your actual backend URL

2. **Environment Variable**: In Vercel dashboard, set:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
   ```

3. **Deploy**: Push to GitHub - Vercel will auto-deploy

## Local Development

```bash
# Backend
cd api
pip install -r requirements.txt
uvicorn app:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

## Architecture Benefits

- **Scalability**: Frontend and backend scale independently
- **Cost**: Pay only for actual backend usage
- **Performance**: Frontend served from Vercel's global CDN
- **Flexibility**: Can easily switch backend hosting providers
- **Development**: Easier to work on frontend/backend separately

## Troubleshooting

- **CORS Issues**: Backend includes CORS middleware for all origins
- **API Connection**: Check `NEXT_PUBLIC_API_URL` environment variable
- **Health Check**: Visit `{backend-url}/api/health` to verify backend is running 