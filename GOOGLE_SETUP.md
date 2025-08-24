# Google Docs API Setup Guide

## Overview
Your CrewAI agents now create documents directly in Google Docs! The Document Publisher agent will create Google Docs with your research results.

## Setup Options

### Option 1: Service Account (Recommended)

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project or select an existing one
3. Enable the "Google Docs API" and "Google Drive API"
4. Go to "Credentials" → "Create Credentials" → "Service Account"
5. Create a service account and download the JSON key file
6. Place the JSON file in your project directory
7. Update `.env`:
   ```
   GOOGLE_SERVICE_ACCOUNT_PATH=path/to/your/service-account.json
   ```

### Option 2: OAuth Credentials

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Enable "Google Docs API" and "Google Drive API"
3. Create OAuth 2.0 credentials
4. Get your refresh token using OAuth flow
5. Update `.env`:
   ```
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   GOOGLE_REFRESH_TOKEN=your_refresh_token
   ```

## Required Dependencies

Install Google API client:

```bash
pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

## Features

- **GoogleDocsCreatorTool**: Creates formatted Google Docs with markdown support
- **SimpleGoogleDocsCreatorTool**: Creates plain text Google Docs
- **Automatic Integration**: Document Publisher agent creates Google Docs
- **Public Sharing**: Documents are automatically made publicly viewable

## How It Works

1. Research Specialist analyzes your problem
2. Document Publisher formats the solution
3. **NEW**: Document Publisher creates a Google Doc with the results
4. You get a shareable Google Docs link

## Troubleshooting

### If you get authentication errors:
- Verify your service account JSON file path is correct
- Ensure Google Docs API and Drive API are enabled
- Check that your service account has proper permissions

### If you don't want to set up Google Docs:
- The agent will show an informative message about missing credentials
- Local file creation will still work as a fallback
- PDF generation in Streamlit will continue to work

## Cost Information

- Google Docs API: Free for most use cases
- Google Drive API: Free for most use cases
- See [Google Workspace APIs pricing](https://developers.google.com/workspace/pricing) for details
