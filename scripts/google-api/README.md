# Google API Integration - Drive & YouTube

This directory contains Python scripts for authenticating and interacting with Google Drive and YouTube APIs using OAuth 2.0.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Available Scripts](#available-scripts)
- [API Features](#api-features)
- [Security Notes](#security-notes)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This integration provides:
- **Google Drive API**: Upload, download, list, and search files; create folders
- **YouTube Data API**: Access channel info, search videos, manage playlists, read comments
- **OAuth 2.0 Authentication**: Secure authentication with token persistence

## ✅ Prerequisites

- Python 3.7 or higher
- Google Cloud Project with Drive & YouTube APIs enabled
- OAuth 2.0 credentials (already configured in `credentials.json`)

## 📦 Installation

1. **Install required Python packages:**

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

2. **Verify credentials file exists:**

```bash
ls credentials.json
```

The OAuth client ID is already configured:
- **Client ID**: `988966010493-43du2fbcltpeuaet86398p962boak66u.apps.googleusercontent.com`

## ⚙️ Configuration

### OAuth Credentials

The `credentials.json` file contains your OAuth 2.0 client configuration. This file is **committed to the repository** but does not contain sensitive secrets.

### Token Files (Auto-generated)

When you first run any script, you'll be prompted to authenticate in your browser. The following token files will be created and **are excluded from git**:

- `token.pickle` - Google Drive API tokens
- `youtube_token.pickle` - YouTube API tokens

**⚠️ IMPORTANT**: Never commit token files to version control. They are already added to `.gitignore`.

## 🚀 Usage

### Quick Start

Run the example script to test both APIs:

```bash
cd scripts/google-api
python3 example_usage.py
```

This will:
1. Prompt you to authenticate via browser
2. Demonstrate Drive operations (list files, search)
3. Demonstrate YouTube operations (channel info, video search)
4. Show combined workflows (export YouTube data to Drive)

### Individual Scripts

#### Google Drive API

```bash
python3 google_drive_auth.py
```

**Basic operations:**

```python
from google_drive_auth import GoogleDriveAPI

# Initialize
drive = GoogleDriveAPI()

# List files
drive.list_files(page_size=10)

# Search for files
docs = drive.search_files("mimeType='application/pdf'")

# Upload a file
file_id = drive.upload_file('/path/to/file.txt')

# Download a file
drive.download_file('file_id_here', '/path/to/save/file.txt')

# Create a folder
folder_id = drive.create_folder('My New Folder')
```

#### YouTube Data API

```bash
python3 youtube_api_auth.py
```

**Basic operations:**

```python
from youtube_api_auth import YouTubeAPI

# Initialize
youtube = YouTubeAPI()

# Get your channel
channel = youtube.get_my_channel()

# Search videos
videos = youtube.search_videos("Python programming", max_results=10)

# Get video details
video = youtube.get_video_details('video_id_here')

# Get playlist videos
videos = youtube.get_playlist_videos('playlist_id_here')

# Get video comments
comments = youtube.get_video_comments('video_id_here', max_results=20)

# Get your playlists
playlists = youtube.get_my_playlists()
```

## 📚 Available Scripts

| Script | Description |
|--------|-------------|
| `google_drive_auth.py` | Google Drive API client with file operations |
| `youtube_api_auth.py` | YouTube Data API client with video/channel operations |
| `example_usage.py` | Comprehensive examples using both APIs |
| `credentials.json` | OAuth 2.0 client configuration |

## 🔧 API Features

### Google Drive API Features

- ✅ List files with filtering
- ✅ Search files by name, type, content
- ✅ Upload files with resumable uploads
- ✅ Download files
- ✅ Create folders
- ✅ Organize files in folders
- ✅ Get file metadata
- ✅ Full OAuth 2.0 authentication

**Scopes used:**
- `https://www.googleapis.com/auth/drive` (full access)

### YouTube Data API Features

- ✅ Get authenticated user's channel info
- ✅ Search for videos
- ✅ Get video details (views, likes, comments count)
- ✅ Get playlist videos
- ✅ Get video comments
- ✅ Get channel videos
- ✅ List user's playlists
- ✅ Full OAuth 2.0 authentication

**Scopes used:**
- `https://www.googleapis.com/auth/youtube.readonly` (read-only access)
- `https://www.googleapis.com/auth/youtube.force-ssl` (SSL-enforced access)

## 🔒 Security Notes

### What's Safe to Commit

✅ **Safe to commit:**
- `credentials.json` - Contains only client ID and OAuth URIs
- `*.py` scripts
- `README.md` documentation

❌ **NEVER commit:**
- `token.pickle` - Contains access tokens
- `youtube_token.pickle` - Contains access tokens
- `*.json` files with "token" in the name
- Any file containing refresh tokens or access tokens

### Token Security

- Token files are stored locally and persist across sessions
- Tokens automatically refresh when expired
- Tokens are excluded from git via `.gitignore`
- If compromised, revoke access at: https://myaccount.google.com/permissions

## 🔍 Troubleshooting

### Common Issues

#### 1. "credentials.json not found"

**Solution:** Ensure you're running the script from the `scripts/google-api` directory or use absolute paths.

```bash
cd scripts/google-api
python3 google_drive_auth.py
```

#### 2. "Access token expired"

**Solution:** Delete the token file and re-authenticate:

```bash
rm token.pickle
python3 google_drive_auth.py
```

#### 3. "OAuth redirect URI mismatch"

**Solution:** Ensure the Google Cloud Console has these redirect URIs configured:
- `http://localhost:8080/`
- `urn:ietf:wg:oauth:2.0:oob`

#### 4. "API quota exceeded"

**Solution:** YouTube Data API has daily quotas. Check your usage at:
https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas

#### 5. "Module not found" errors

**Solution:** Install required dependencies:

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Enable APIs in Google Cloud Console

If you get "API not enabled" errors:

1. Go to: https://console.cloud.google.com/apis/library
2. Search for "YouTube Data API v3" and enable it
3. Search for "Google Drive API" and enable it

## 📖 Example Use Cases

### 1. Backup YouTube Playlist to Drive

```python
from google_drive_auth import GoogleDriveAPI
from youtube_api_auth import YouTubeAPI

drive = GoogleDriveAPI()
youtube = YouTubeAPI()

# Get playlist
playlist_id = 'YOUR_PLAYLIST_ID'
videos = youtube.get_playlist_videos(playlist_id)

# Create backup file
with open('/tmp/playlist_backup.txt', 'w') as f:
    for video in videos:
        f.write(f"{video['snippet']['title']}\n")

# Upload to Drive
drive.upload_file('/tmp/playlist_backup.txt')
```

### 2. Search and Archive Videos

```python
from youtube_api_auth import YouTubeAPI

youtube = YouTubeAPI()

# Search for educational content
videos = youtube.search_videos("machine learning tutorial", max_results=50)

# Process each video
for video in videos:
    video_id = video['id']['videoId']
    details = youtube.get_video_details(video_id)
    # Archive or process as needed
```

### 3. Channel Analytics Export

```python
from google_drive_auth import GoogleDriveAPI
from youtube_api_auth import YouTubeAPI
import json

drive = GoogleDriveAPI()
youtube = YouTubeAPI()

# Get channel data
channel = youtube.get_my_channel()
playlists = youtube.get_my_playlists()

# Export to JSON
data = {
    'channel': channel,
    'playlists': playlists
}

with open('/tmp/analytics.json', 'w') as f:
    json.dump(data, f, indent=2)

# Upload to Drive
drive.upload_file('/tmp/analytics.json')
```

## 📞 Support

For issues with:
- **Google APIs**: https://developers.google.com/youtube/v3/support
- **OAuth 2.0**: https://developers.google.com/identity/protocols/oauth2

## 📄 License

This integration is part of the Obsidian Vault project.

## 🔗 Useful Links

- [Google Drive API Documentation](https://developers.google.com/drive/api/guides/about-sdk)
- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)
- [API Quotas and Limits](https://developers.google.com/youtube/v3/getting-started#quota)

---

**Last Updated**: November 2025
**OAuth Client ID**: `988966010493-43du2fbcltpeuaet86398p962boak66u.apps.googleusercontent.com`
