# Environment Variables for Railway Deployment

## Quick Copy-Paste for Railway Variables

When setting up your Railway project, add these environment variables:

```
GOOGLE_API_KEY
TEXT_MODEL
IMAGE_MODEL
TIMEOUT_SECS
PORT
```

## Variable Values

### GOOGLE_API_KEY
- **Value**: Your actual Google API key from https://aistudio.google.com/app/apikey
- **Required**: Yes
- **Example**: `AIzaSyAO4XjtxJBD8JXPWUtBQRZB5KzJHHSu0R8`
- **Important**: Never commit this to git!

### TEXT_MODEL
- **Value**: `gemini-2.0-flash-exp`
- **Required**: Yes
- **Purpose**: Gemini model for generating text content (NZSL prompts, activities, story frames)

### IMAGE_MODEL  
- **Value**: `gemini-2.5-flash-image`
- **Required**: Yes
- **Purpose**: Gemini model for generating the 4 learning images

### TIMEOUT_SECS
- **Value**: `60`
- **Required**: No (defaults to 60)
- **Purpose**: API request timeout in seconds
- **Note**: May need to increase to 90-120 if experiencing timeouts

### PORT
- **Value**: `8000`
- **Required**: No (Railway sets this automatically)
- **Purpose**: Port the application listens on
- **Note**: Railway will override this with $PORT environment variable

## How Variables Are Used

The application reads these variables in `backend/settings.py`:

```python
class Settings(BaseSettings):
    google_api_key: str
    text_model: str = "gemini-2.0-flash-exp"
    image_model: str = "gemini-2.5-flash-image"
    timeout_secs: int = 60
```

Pydantic automatically:
1. Checks for variables in environment
2. Falls back to .env file (local development only)
3. Uses default values if specified

## Local Development

For local development, create a `.env` file (already in .gitignore):

```bash
cp .env.example .env
# Edit .env and add your real GOOGLE_API_KEY
```

## Railway Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created and linked to GitHub repo
- [ ] All environment variables set in Railway dashboard
- [ ] Build command configured (if not auto-detected)
- [ ] Start command configured (if not auto-detected)
- [ ] Deployment successful
- [ ] Test URL works and generates packs

## Security Notes

✅ **Safe to commit**:
- `.env.example` (template with placeholder values)
- `settings.py` (reads from environment, no secrets)
- `railway.json` (configuration only)

❌ **Never commit**:
- `.env` (contains your actual API key)
- Any file with real API keys
