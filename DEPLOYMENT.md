# 🚀 Deployment Guide - Multiple Platform Options

This application uses a split deployment strategy:
- **Frontend**: Multiple options available
- **Backend**: Multiple options (pick your favorite!)

## 🏆 **FULL AWS DEPLOYMENT (Recommended)**

**Why deploy everything on AWS:**
- 🔗 **Better integration** between services
- 💰 **Cost optimization** (no cross-cloud transfer)
- 📊 **Unified monitoring** and logs
- 🛡️ **Enterprise-ready** architecture

### **Step 1: Deploy Backend on App Runner**
1. **AWS App Runner Console** → Create Service
2. **Connect GitHub repo**
3. **Configure build**:
   - Build command: `cd api && pip install -r requirements.txt`
   - Start command: `cd api && python app.py`
   - Port: `8000`
4. **Deploy and get URL** (e.g., `https://abc123.us-east-1.awsapprunner.com`)

### **Step 2: Deploy Frontend on Amplify**
1. **AWS Amplify Console** → New App → Connect GitHub
2. **Select your repo** and main branch
3. **Auto-detect build** (uses `amplify.yml`)
4. **Add environment variable**:
   ```
   NEXT_PUBLIC_API_URL=https://your-app-runner-url.amazonaws.com
   ```
5. **Deploy!** 🚀

### **Cost for Full AWS (Monthly)**
- **App Runner**: $0 (free tier: 2M requests)
- **Amplify**: $0 (free tier: 15GB)
- **Total**: **$0** for demos/low traffic! 🎉

---

## 🥇 **Option 1: Render (Recommended)**

**Why Render rocks:**
- 🆓 Generous free tier (750 hours/month)
- 🔄 Auto-deploy from GitHub
- 🐳 Native Docker support
- 📊 Great for demos and production

### Steps:
1. **Fork & Connect**: Fork this repo, sign up at [render.com](https://render.com)
2. **Create Web Service**: Click "New" → "Web Service" → Connect GitHub repo
3. **Config**: Render auto-detects the `render.yaml` file
4. **Deploy**: Click "Create Web Service" - that's it! 🎉
5. **Get URL**: Copy your Render URL (e.g., `https://banker-wingman-api.onrender.com`)

---

## 🔥 **Option 2: Fly.io (Performance Beast)**

**Perfect for production apps needing speed:**

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy (it's this easy!)
fly launch
fly deploy

# Get your URL
fly status
```

---

## ⭐ **Option 3: Google Cloud Run (Enterprise)**

**For serious production deployments:**

```bash
# Enable APIs and set project
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com

# Deploy
gcloud run deploy banker-wingman \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🌊 **Option 4: DigitalOcean App Platform**

**Simple and reliable:**

1. Sign up at [DigitalOcean](https://digitalocean.com)
2. Go to Apps → Create App → GitHub repo
3. It auto-detects Dockerfile and deploys
4. Starting at $5/month

---

## 🐙 **Option 5: Heroku (Classic)**

```bash
# Install Heroku CLI, then:
heroku create banker-wingman-api
heroku stack:set container
git push heroku main
```

---

## 🎯 **Frontend Deployment Options**

### **AWS Amplify (Full AWS Setup)**
1. **Connect GitHub** to AWS Amplify
2. **Auto-detect** build settings (`amplify.yml`)
3. **Set environment variable**: `NEXT_PUBLIC_API_URL`
4. **Deploy automatically** 🚀

### **Vercel (Works with ANY Backend)**
1. **Update API URL**: Edit `vercel.json` and replace the destination URL:
   ```json
   {
     "projectPath": "frontend",
     "rewrites": [
       {
         "source": "/api/(.*)",
         "destination": "https://YOUR-BACKEND-URL/api/$1"
       }
     ]
   }
   ```

2. **Environment Variable**: In Vercel dashboard, set:
   ```
   NEXT_PUBLIC_API_URL=https://YOUR-BACKEND-URL
   ```

3. **Deploy**: Connect GitHub repo to Vercel and deploy! 🚀

---

## 💰 **Cost Comparison**

| Platform | Free Tier | Paid Starts At | Best For |
|----------|-----------|----------------|----------|
| **AWS Full Stack** | 2M requests + 15GB | $0.01/request + $0.01/GB | **Enterprise** |
| **Render** | 750 hrs/month | $7/month | **Demos & Small Apps** |
| **Fly.io** | 3 VMs free | $1.94/month | **Performance Apps** |
| **Cloud Run** | 2M requests/month | Pay-per-use | **Enterprise** |
| **DigitalOcean** | $200 credit | $5/month | **Predictable Costs** |
| **Railway** | $5 credit | $5/month | **Simple Deploys** |

---

## 🛠️ **Local Development**

```bash
# Backend (pick any terminal)
cd api
pip install -r requirements.txt
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` and code away! 🎯

---

## 🔧 **Environment Variables**

### Backend (All Platforms)
```bash
PORT=8000                  # Auto-set by most platforms
OPENAI_API_KEY=sk-...     # Optional - users provide their own
```

### Frontend
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

---

## 🐛 **Troubleshooting All Platforms**

**Backend Issues:**
- **Health check failing** → Ensure `/api/health` endpoint works
- **Port binding errors** → Check if platform sets PORT env var
- **Build failures** → Verify Dockerfile and requirements.txt

**Frontend Issues:**
- **API not connecting** → Double-check `NEXT_PUBLIC_API_URL`
- **CORS errors** → Backend includes CORS middleware for all origins
- **Build errors** → Check Node.js version (need 18+)

**Platform Specific:**
- **AWS**: Check CloudWatch logs
- **Render**: Check build logs in dashboard
- **Fly.io**: Use `fly logs` to debug
- **Cloud Run**: Check Cloud Console logs
- **Railway**: View logs in dashboard

---

## 🎉 **Success Checklist**

✅ Backend deployed and `/api/health` returns OK  
✅ Frontend deployed and loads properly  
✅ API calls work from frontend to backend  
✅ File upload and RAG functionality working  
✅ OpenAI API key validation works  

**You're live! 🚀** Share your creation with the world!

---

*Pro tip: For production apps, go with full AWS (App Runner + Amplify) for the best integration and cost optimization! 🎯* 