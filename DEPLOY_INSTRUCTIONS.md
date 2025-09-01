# Deployment Instructions

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository named `breese-prompter`
3. Make it public or private (your choice)
4. DON'T initialize with README (we already have one)

## Step 2: Push to GitHub

Run these commands in your terminal:

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/breese-prompter.git

# Push to GitHub
git push -u origin main
```

## Step 3: Deploy to Render

1. Go to https://render.com
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub account if not already connected
5. Select the `breese-prompter` repository
6. Render will auto-detect the configuration from `render.yaml`
7. Add Environment Variable:
   - Key: `OPENROUTER_API_KEY`
   - Value: Your OpenRouter API key (from https://openrouter.ai/keys)
8. Click "Create Web Service"

## Step 4: Wait for Deployment

- Render will build and deploy your service
- This takes about 5-10 minutes
- Your API will be available at: `https://breese-prompter.onrender.com` (or similar)

## Step 5: Test Your Deployment

```bash
# Test the health endpoint
curl https://your-service.onrender.com/api/health

# Test the API docs
# Visit: https://your-service.onrender.com/docs
```

## Step 6: Use in ChatGPT

1. Go to ChatGPT → Create GPT
2. Add Action → Import from URL
3. Enter: `https://your-service.onrender.com/openapi.json`
4. Configure authentication if needed
5. Test with sample prompts!

## Environment Variables Needed

- `OPENROUTER_API_KEY`: Required - Get from https://openrouter.ai/keys

## Optional: Custom Domain

In Render dashboard:
1. Go to Settings → Custom Domains
2. Add your domain
3. Configure DNS as instructed

## Monitoring

- Check logs in Render dashboard
- Monitor API usage in OpenRouter dashboard
- Set up alerts if needed

## Updates

To deploy updates:
1. Make changes locally
2. Commit: `git add . && git commit -m "Update message"`
3. Push: `git push origin main`
4. Render will auto-deploy!

## Troubleshooting

If deployment fails:
1. Check Render logs for errors
2. Verify OPENROUTER_API_KEY is set correctly
3. Ensure Python version matches (3.11.0)
4. Check requirements.txt for issues

## Support

- Render Docs: https://render.com/docs
- OpenRouter Docs: https://openrouter.ai/docs
- FastAPI Docs: https://fastapi.tiangolo.com