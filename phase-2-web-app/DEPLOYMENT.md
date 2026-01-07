# 🚀 Deployment Guide - Todo App

Complete guide for deploying the FastAPI backend and Next.js frontend to production.

---

## 📊 Deployment Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Vercel        │─────▶│  Render/Railway  │─────▶│ Neon PostgreSQL │
│  (Frontend)     │ HTTPS │   (Backend API)  │ SSL  │   (Database)    │
│   Next.js       │◀─────│    FastAPI       │◀─────│                 │
└─────────────────┘      └──────────────────┘      └─────────────────┘
```

---

## 🎯 Recommended Options

### Option 1: FREE Tier (Best for Testing/Learning)
- **Backend**: Render.com (Free)
- **Frontend**: Vercel (Free)
- **Database**: Neon PostgreSQL (Free tier - already configured)

### Option 2: Production (Best Performance)
- **Backend**: Railway ($5-10/month)
- **Frontend**: Vercel (Free)
- **Database**: Neon PostgreSQL (Free tier or paid)

---

## 📦 Part 1: Backend Deployment

### Step 1: Prepare Backend Files

#### 1.1 Create `requirements.txt`

Your backend needs a `requirements.txt` for deployment. Check if it exists:

```bash
cd phase-2-web-app/backend
cat requirements.txt
```

If missing or incomplete, create it with:

```txt
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlmodel>=0.0.14
asyncpg>=0.29.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
alembic>=1.13.0
python-dotenv>=1.0.0
```

#### 1.2 Create `Procfile` (for Render)

```bash
# phase-2-web-app/backend/Procfile
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### 1.3 Create `railway.json` (for Railway - optional)

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 1.4 Create `runtime.txt` (specify Python version)

```txt
python-3.13
```

---

### Step 2A: Deploy to Render (FREE Option)

#### 2.1 Sign up for Render
1. Go to https://render.com
2. Sign up with GitHub
3. Connect your repository

#### 2.2 Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select the repository: `HackathonII-TODO-APP`
4. Configure:
   - **Name**: `todo-api` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `phase-2-web-app/backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

#### 2.3 Set Environment Variables
In Render dashboard, add these environment variables:

```
DATABASE_URL=postgresql+asyncpg://neondb_owner:npg_HvxfMqG5Fb7Y@ep-withered-sunset-a1kv12v0-pooler.ap-southeast-1.aws.neon.tech/neondb

BETTER_AUTH_SECRET=b0e3cc396c2f15582a8f6ca6d0a2cb5f32e227cdd6e1d02d5517e215721f225c

CORS_ORIGINS=https://your-frontend-url.vercel.app,http://localhost:3000

DEBUG=False
```

**Important**: Update `CORS_ORIGINS` with your actual Vercel URL after frontend deployment.

#### 2.4 Deploy
- Click **"Create Web Service"**
- Wait for build to complete (3-5 minutes)
- Your API will be live at: `https://todo-api.onrender.com`

---

### Step 2B: Deploy to Railway (PAID Option - Better Performance)

#### 2.1 Sign up for Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Add payment method (required even for trial)

#### 2.2 Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository
4. Railway will auto-detect the Python app

#### 2.3 Configure Service
1. Click on the service
2. Go to **Settings**
3. Set:
   - **Root Directory**: `phase-2-web-app/backend`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### 2.4 Set Environment Variables
In Railway dashboard, add:

```
DATABASE_URL=postgresql+asyncpg://neondb_owner:npg_HvxfMqG5Fb7Y@ep-withered-sunset-a1kv12v0-pooler.ap-southeast-1.aws.neon.tech/neondb

BETTER_AUTH_SECRET=b0e3cc396c2f15582a8f6ca6d0a2cb5f32e227cdd6e1d02d5517e215721f225c

CORS_ORIGINS=https://your-frontend-url.vercel.app,http://localhost:3000

DEBUG=False
```

#### 2.5 Generate Domain
1. Go to **Settings** → **Networking**
2. Click **"Generate Domain"**
3. Your API will be at: `https://your-app.railway.app`

---

## 🎨 Part 2: Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

#### 1.1 Update Environment Variables

Create/update `phase-2-web-app/frontend/.env.production`:

```env
# Production backend API URL (update after backend deployment)
NEXT_PUBLIC_API_URL=https://todo-api.onrender.com

# OR for Railway:
# NEXT_PUBLIC_API_URL=https://your-app.railway.app

NODE_ENV=production
```

#### 1.2 Verify Build Configuration

Check `phase-2-web-app/frontend/next.config.js`:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone', // Optimized for deployment
  reactStrictMode: true,
  swcMinify: true,
}

module.exports = nextConfig
```

### Step 2: Deploy to Vercel

#### 2.1 Sign up for Vercel
1. Go to https://vercel.com
2. Sign up with GitHub
3. Import your repository

#### 2.2 Configure Project
1. Click **"Add New..."** → **"Project"**
2. Import `HackathonII-TODO-APP` repository
3. Configure:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `phase-2-web-app/frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `.next` (auto-detected)
   - **Install Command**: `npm install` (auto-detected)

#### 2.3 Add Environment Variables
In Vercel project settings, add:

```
NEXT_PUBLIC_API_URL=https://todo-api.onrender.com
```

(Use your actual backend URL from Render/Railway)

#### 2.4 Deploy
- Click **"Deploy"**
- Wait 2-3 minutes
- Your app will be live at: `https://your-app.vercel.app`

---

## 🔄 Part 3: Connect Frontend & Backend

### Step 1: Update Backend CORS

After frontend deployment, update backend `CORS_ORIGINS`:

**On Render:**
1. Go to Render dashboard
2. Select your backend service
3. Go to **Environment**
4. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000
   ```
5. Save (this will trigger auto-redeploy)

**On Railway:**
1. Go to Railway dashboard
2. Select your backend service
3. Go to **Variables**
4. Update `CORS_ORIGINS`
5. Redeploy

### Step 2: Test the Connection

1. Open your Vercel URL: `https://your-app.vercel.app`
2. Try to sign up/login
3. Check browser console for errors
4. Verify API calls are going to your backend URL

---

## ✅ Deployment Checklist

### Backend Checklist
- [ ] `requirements.txt` exists and is complete
- [ ] `Procfile` created (for Render)
- [ ] Environment variables configured
- [ ] `DEBUG=False` in production
- [ ] CORS origins include your Vercel URL
- [ ] Database migrations run (if needed)
- [ ] Backend is accessible at `/docs` (Swagger UI)
- [ ] Health check endpoint works: `GET /`

### Frontend Checklist
- [ ] `NEXT_PUBLIC_API_URL` points to backend
- [ ] Build succeeds locally: `npm run build`
- [ ] Environment variables set in Vercel
- [ ] No hardcoded localhost URLs in code
- [ ] CORS allows requests from Vercel domain

---

## 🐛 Troubleshooting

### Backend Issues

**Problem: Backend is sleeping (Render free tier)**
- Solution: Upgrade to paid tier OR use Railway OR ping your backend every 10 minutes with a cron job

**Problem: CORS errors**
```
Access to fetch at 'https://api...' from origin 'https://app...' has been blocked by CORS
```
- Solution: Add your Vercel URL to `CORS_ORIGINS` in backend environment variables

**Problem: Database connection fails**
- Check `DATABASE_URL` is correct in backend env vars
- Verify Neon database is accessible
- Check if asyncpg is installed: `asyncpg>=0.29.0`

### Frontend Issues

**Problem: API calls fail**
- Check `NEXT_PUBLIC_API_URL` is set correctly
- Verify backend is running and accessible
- Check browser console for actual error

**Problem: Environment variables not loaded**
- In Vercel, environment variables must start with `NEXT_PUBLIC_` to be exposed to browser
- Redeploy after adding environment variables

---

## 📊 Cost Breakdown

### FREE Tier (Option 1)
- Backend (Render): **$0/month** (with sleep)
- Frontend (Vercel): **$0/month**
- Database (Neon): **$0/month** (0.5 GB storage)
- **Total: $0/month** ✅

### Paid Tier (Option 2)
- Backend (Railway): **$5-10/month** (no sleep)
- Frontend (Vercel): **$0/month**
- Database (Neon): **$0/month** (or $19/month for more)
- **Total: ~$5-10/month**

---

## 🚀 Quick Deploy Commands

### Backend (Render)
```bash
cd phase-2-web-app/backend

# Ensure requirements.txt is up to date
pip freeze > requirements.txt

# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Commit and push
git add .
git commit -m "chore: prepare backend for Render deployment"
git push
```

### Frontend (Vercel)
```bash
cd phase-2-web-app/frontend

# Test build locally
npm run build

# Create production env
echo "NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com" > .env.production

# Commit and push
git add .
git commit -m "chore: prepare frontend for Vercel deployment"
git push
```

---

## 📚 Additional Resources

- **Render Documentation**: https://render.com/docs/deploy-fastapi
- **Railway Documentation**: https://docs.railway.app/deploy/deployments
- **Vercel Documentation**: https://vercel.com/docs/frameworks/nextjs
- **Neon Documentation**: https://neon.tech/docs/introduction

---

## 🆘 Need Help?

If you encounter issues:
1. Check deployment logs in Render/Railway/Vercel dashboard
2. Verify all environment variables are set correctly
3. Test backend API directly using `/docs` endpoint
4. Check browser console for frontend errors

---

**Last Updated**: 2026-01-08
**Project**: Todo Manager - Phase II Web Application
