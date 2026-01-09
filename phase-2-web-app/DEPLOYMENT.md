# Deployment Guide - Phase II Web Application

This guide provides step-by-step instructions for deploying the Todo Manager web application to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Deployment (Railway)](#backend-deployment-railway)
3. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
4. [Post-Deployment Configuration](#post-deployment-configuration)
5. [Verification & Testing](#verification--testing)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts

1. **GitHub Account** - For repository hosting
2. **Neon Account** - For PostgreSQL database ([neon.tech](https://neon.tech))
3. **Railway Account** - For backend hosting ([railway.app](https://railway.app))
4. **Vercel Account** - For frontend hosting ([vercel.com](https://vercel.com))

### Required Tools

- Git installed locally
- Node.js 18.x or higher
- Python 3.13 or higher (for local testing)

---

## Backend Deployment (Railway)

### Step 1: Set Up Database (Neon PostgreSQL)

1. **Create Neon Account**
   - Go to [neon.tech](https://neon.tech)
   - Sign up with GitHub or email

2. **Create New Project**
   - Click "Create Project"
   - Name: \`todo-app-production\`
   - Region: Choose closest to your users (e.g., US East)
   - PostgreSQL version: 16 (latest)

3. **Get Connection String**
   - Go to project dashboard
   - Copy the connection string
   - **Important**: Change the protocol from \`postgresql://\` to \`postgresql+asyncpg://\`

   **Example:**
   \`\`\`
   Original: postgresql://username:password@ep-cool-smoke-123456.us-east-2.aws.neon.tech/neondb
   Updated:  postgresql+asyncpg://username:password@ep-cool-smoke-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
   \`\`\`

4. **Save Connection String**
   - Keep this for Railway environment variables

### Step 2: Generate Secrets

Generate secure secrets for authentication:

\`\`\`bash
# Generate BETTER_AUTH_SECRET (minimum 32 characters)
openssl rand -hex 32

# Generate JWT_SECRET (minimum 32 characters)
openssl rand -hex 32
\`\`\`

**Save these secrets** - you'll need the same \`BETTER_AUTH_SECRET\` for both backend and frontend!

### Step 3: Deploy to Railway

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your repository
   - Select your repository

3. **Configure Service**
   - Railway will detect the backend automatically
   - Service name: \`todo-backend\`
   - Root directory: \`Phase-2-Web-App/backend\`

4. **Set Environment Variables**

   Go to service → Variables → Add variables:

   \`\`\`bash
   DATABASE_URL=postgresql+asyncpg://your-connection-string-from-neon
   BETTER_AUTH_SECRET=your-generated-secret-from-step-2
   JWT_SECRET=your-generated-jwt-secret-from-step-2
   CORS_ORIGINS=http://localhost:3000
   DEBUG=False
   JWT_ALGORITHM=HS256
   \`\`\`

   **Note**: We'll update \`CORS_ORIGINS\` after deploying the frontend.

5. **Deploy**
   - Click "Deploy"
   - Railway will automatically install dependencies and run
   - Wait for deployment to complete (2-5 minutes)

6. **Get Backend URL**
   - Once deployed, Railway provides a URL
   - Click "Generate Domain" if not automatically created
   - **Save this URL** for frontend configuration

7. **Verify Deployment**
   - Open \`https://your-backend-url.railway.app/\`
   - You should see: \`{"status":"ok","message":"Todo API is running"}\`

---

## Frontend Deployment (Vercel)

### Step 1: Deploy to Vercel

1. **Create Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Import Project**
   - Click "Add New" → "Project"
   - Import your repository
   - Framework Preset: **Next.js** (auto-detected)

3. **Configure Build Settings**
   - Root Directory: \`Phase-2-Web-App/frontend\`
   - Framework: Next.js
   - Build Command: \`npm run build\`
   - Node.js Version: 18.x

4. **Set Environment Variables**

   Click "Environment Variables" and add:

   \`\`\`bash
   NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
   BETTER_AUTH_SECRET=your-same-secret-from-railway
   BETTER_AUTH_URL=https://your-frontend-url.vercel.app
   NODE_ENV=production
   \`\`\`

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment (2-3 minutes)

6. **Get Frontend URL**
   - Once deployed, Vercel provides a URL
   - **Save this URL**

---

## Post-Deployment Configuration

### Step 1: Update Backend CORS

1. Go to Railway → Your service → Variables
2. Update \`CORS_ORIGINS\`:
   \`\`\`bash
   CORS_ORIGINS=https://your-actual-frontend.vercel.app
   \`\`\`

### Step 2: Update Frontend BETTER_AUTH_URL

1. Go to Vercel → Settings → Environment Variables
2. Update \`BETTER_AUTH_URL\` with your actual Vercel URL

---

## Verification & Testing

### Test Backend API

\`\`\`bash
curl https://your-backend.railway.app/
# Should return: {"status":"ok","message":"Todo API is running"}
\`\`\`

### Test Frontend

1. Visit your Vercel URL
2. Sign up for a new account
3. Create a test task
4. Verify everything works

---

## Troubleshooting

### Backend Issues

**CORS errors**: Verify \`CORS_ORIGINS\` includes your Vercel URL

**Database connection fails**: Check connection string uses \`postgresql+asyncpg://\` and \`?sslmode=require\`

**500 errors**: Check Railway logs

### Frontend Issues

**API calls fail**: Verify \`NEXT_PUBLIC_API_URL\` is correct

**Auth fails**: Verify \`BETTER_AUTH_SECRET\` matches backend

---

**Deployment Complete!** 🚀

For detailed troubleshooting and advanced configuration, see the full documentation.
