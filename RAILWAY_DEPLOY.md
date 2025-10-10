# Railway Deployment Guide for Tohu Kaiako

## Prerequisites
- Railway account (sign up at https://railway.app)
- Google API key for Gemini (get from https://aistudio.google.com/app/apikey)

## Environment Variables

Set these in your Railway project settings:

### Required Variables

```bash
GOOGLE_API_KEY=your_actual_google_api_key_here
TEXT_MODEL=gemini-2.0-flash-exp
IMAGE_MODEL=gemini-2.5-flash-image
TIMEOUT_SECS=60
PORT=8000
```

## Quick Deploy Steps

### Option 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub** (already done if you're reading this)

2. **Create a new Railway project**:
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `craigjefferies/Tohu-Kaiako`

3. **Configure Environment Variables**:
   - In your Railway project, go to "Variables"
   - Add each variable from the list above
   - **IMPORTANT**: Replace `your_actual_google_api_key_here` with your real API key

4. **Configure Build & Deploy**:
   - Railway should auto-detect Python
   - Build Command: `cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt`
   - Start Command: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`

5. **Deploy**:
   - Railway will automatically deploy on push to main branch
   - Get your public URL from Railway dashboard

### Option 2: Deploy using Railway CLI

1. **Install Railway CLI**:
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize project**:
   ```bash
   railway init
   ```

4. **Set environment variables**:
   ```bash
   railway variables set GOOGLE_API_KEY="your_actual_google_api_key_here"
   railway variables set TEXT_MODEL="gemini-2.0-flash-exp"
   railway variables set IMAGE_MODEL="gemini-2.5-flash-image"
   railway variables set TIMEOUT_SECS="60"
   railway variables set PORT="8000"
   ```

5. **Deploy**:
   ```bash
   railway up
   ```

## Verifying Deployment

Once deployed, visit your Railway URL and:
1. Enter a theme like "Kererū in the forest"
2. Click "Generate Pack"
3. Wait 30-60 seconds for images to generate
4. Verify all sections appear:
   - Scene Preview Strip
   - Learning Image Set
   - Scene Components
   - Story Frames
   - Activity Web

## Troubleshooting

### "API Key not found" error
- Verify `GOOGLE_API_KEY` is set in Railway variables
- Check the key is valid at https://aistudio.google.com/app/apikey

### Build fails
- Check that `requirements.txt` and `package.json` are in the repo
- Verify Python version compatibility (3.11+)

### Images not generating
- Check Railway logs for API errors
- Verify `IMAGE_MODEL` is set to `gemini-2.5-flash-image`
- Ensure your Google API key has Gemini API access enabled

### Timeout errors
- Increase `TIMEOUT_SECS` to 90 or 120
- Check Railway resource limits

## Cost Considerations

- **Railway**: Free tier available, then pay-as-you-go
- **Google Gemini API**: 
  - Free tier: 15 requests per minute, 1500 per day
  - Paid tier: Check current pricing at https://ai.google.dev/pricing

## Monitoring

- View logs: Railway dashboard → Your project → Deployments → View logs
- Check metrics: Railway dashboard → Your project → Metrics

## Updating

When you push changes to GitHub main branch, Railway will automatically:
1. Pull the latest code
2. Rebuild the application
3. Redeploy with zero downtime

## Support

For issues specific to:
- **Railway deployment**: https://railway.app/help
- **Google Gemini API**: https://ai.google.dev/gemini-api/docs
- **This application**: Create an issue on GitHub
