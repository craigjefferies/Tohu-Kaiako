# Google Vertex AI Imagen Setup Guide

This guide will help you set up Google Vertex AI Imagen for image generation in Tohu-Kaiako.

## Prerequisites

- Google Cloud account
- Billing enabled on your Google Cloud project
- Google Cloud CLI installed (optional, for testing)

## Step 1: Set Up Google Cloud Project

1. **Go to Google Cloud Console**: https://console.cloud.google.com/

2. **Create or select a project**:
   - Click on the project dropdown at the top
   - Create a new project or select an existing one
   - Note your **Project ID** (you'll need this)

3. **Enable billing**:
   - Go to **Billing** in the left menu
   - Link a billing account to your project
   - Imagen API requires billing to be enabled

## Step 2: Enable Required APIs

1. **Go to APIs & Services > Library**:
   - Search for "Vertex AI API"
   - Click **Enable**
   
2. **Enable Imagen API**:
   - Search for "Vertex AI Imagen API" or "Cloud AI Platform"
   - Click **Enable**

## Step 3: Set Up Authentication

### Option A: Using Service Account (Recommended for Production)

1. **Create a Service Account**:
   - Go to **IAM & Admin > Service Accounts**
   - Click **Create Service Account**
   - Name: `tohu-kaiako-imagen`
   - Click **Create and Continue**

2. **Grant Permissions**:
   - Add role: **Vertex AI User**
   - Click **Continue** then **Done**

3. **Create JSON Key**:
   - Click on your service account
   - Go to **Keys** tab
   - Click **Add Key > Create new key**
   - Select **JSON**
   - Download the key file
   - **Save it securely** - you'll use this for authentication

4. **Update your `.env` file**:
   ```bash
   GOOGLE_CLOUD_PROJECT_ID=your-project-id
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-service-account-key.json
   ```

### Option B: Using Application Default Credentials (For Development)

1. **Install Google Cloud CLI**: https://cloud.google.com/sdk/docs/install

2. **Authenticate**:
   ```bash
   gcloud auth application-default login
   ```

3. **Set your project**:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

4. **Update your `.env` file**:
   ```bash
   GOOGLE_CLOUD_PROJECT_ID=your-project-id
   ```

## Step 4: Install Required Python Package

The Vertex AI SDK is needed for Imagen:

```bash
pip install google-cloud-aiplatform
```

## Step 5: Update Application Code

Once billing is set up, we'll update the `backend/llm.py` file to use Vertex AI Imagen instead of placeholders.

## Pricing Information

**Imagen Pricing (as of 2024)**:
- Standard quality: ~$0.02 per image
- High quality: ~$0.04 per image
- Pricing may vary by region

Check current pricing: https://cloud.google.com/vertex-ai/pricing#imagen

## Testing Your Setup

You can test Vertex AI Imagen with this command:

```bash
python3 << 'EOF'
from google.cloud import aiplatform
from vertexai.preview.vision_models import ImageGenerationModel

# Initialize Vertex AI
aiplatform.init(project='YOUR_PROJECT_ID', location='us-central1')

# Load the model
model = ImageGenerationModel.from_pretrained("imagegeneration@006")

# Generate an image
images = model.generate_images(
    prompt="A simple, bold, clear illustration of a fantail bird in a garden for a 4-year-old child",
    number_of_images=1,
)

print(f"Generated {len(images)} image(s)")
print(f"Image size: {images[0]._image_bytes.__sizeof__()} bytes")
EOF
```

## Next Steps

Once you have:
1. ✅ Billing enabled
2. ✅ Vertex AI API enabled
3. ✅ Service account created (or gcloud auth set up)
4. ✅ Project ID noted

Let me know and I'll update the code to use Vertex AI Imagen!

## Troubleshooting

**Error: "Billing not enabled"**
- Make sure billing is enabled on your project
- Check that the billing account is active

**Error: "Permission denied"**
- Ensure your service account has "Vertex AI User" role
- Check that the API is enabled

**Error: "Model not found"**
- Imagen may not be available in all regions
- Try region: `us-central1` (most common)

## Security Notes

- **Never commit** your service account JSON key to git
- Add `*.json` to `.gitignore` for service account keys
- Rotate keys periodically
- Use environment variables for credentials
