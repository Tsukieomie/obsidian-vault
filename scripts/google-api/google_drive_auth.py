#!/usr/bin/env python3
"""
Google Drive API Authentication and Access Script

This script authenticates with Google Drive API using OAuth 2.0 and provides
basic functionality to list, upload, and download files from Google Drive.

Requirements:
    pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

# Define the scopes for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(SCRIPT_DIR, 'token.pickle')


class GoogleDriveAPI:
    """Google Drive API wrapper class"""

    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with Google Drive API"""
        # Token file stores the user's access and refresh tokens
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                self.creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                self.creds = flow.run_local_server(port=8080)

            # Save the credentials for the next run
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(self.creds, token)

        # Build the service
        self.service = build('drive', 'v3', credentials=self.creds)
        print("✓ Successfully authenticated with Google Drive API")

    def list_files(self, page_size=10, query=None):
        """
        List files from Google Drive

        Args:
            page_size: Number of files to list (default: 10)
            query: Search query (e.g., "mimeType='image/jpeg'")

        Returns:
            List of file metadata dictionaries
        """
        try:
            results = self.service.files().list(
                pageSize=page_size,
                q=query,
                fields="nextPageToken, files(id, name, mimeType, size, createdTime, modifiedTime)"
            ).execute()

            items = results.get('files', [])

            if not items:
                print('No files found.')
                return []

            print(f'\nFound {len(items)} files:')
            for item in items:
                size = int(item.get('size', 0)) if item.get('size') else 0
                size_mb = size / (1024 * 1024)
                print(f"  - {item['name']} ({item['mimeType']}) - {size_mb:.2f} MB")
                print(f"    ID: {item['id']}")

            return items

        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def upload_file(self, file_path, folder_id=None):
        """
        Upload a file to Google Drive

        Args:
            file_path: Local path to the file to upload
            folder_id: Optional folder ID to upload to

        Returns:
            File ID of the uploaded file
        """
        try:
            file_name = os.path.basename(file_path)
            file_metadata = {'name': file_name}

            if folder_id:
                file_metadata['parents'] = [folder_id]

            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()

            print(f"✓ File uploaded successfully: {file.get('name')}")
            print(f"  File ID: {file.get('id')}")
            print(f"  View link: {file.get('webViewLink')}")

            return file.get('id')

        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def download_file(self, file_id, output_path):
        """
        Download a file from Google Drive

        Args:
            file_id: ID of the file to download
            output_path: Local path where to save the file

        Returns:
            True if successful, False otherwise
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)

            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download progress: {int(status.progress() * 100)}%")

            # Write to file
            with open(output_path, 'wb') as f:
                f.write(file.getvalue())

            print(f"✓ File downloaded successfully to: {output_path}")
            return True

        except HttpError as error:
            print(f'An error occurred: {error}')
            return False

    def create_folder(self, folder_name, parent_folder_id=None):
        """
        Create a folder in Google Drive

        Args:
            folder_name: Name of the folder to create
            parent_folder_id: Optional parent folder ID

        Returns:
            Folder ID of the created folder
        """
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }

            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]

            folder = self.service.files().create(
                body=file_metadata,
                fields='id, name'
            ).execute()

            print(f"✓ Folder created successfully: {folder.get('name')}")
            print(f"  Folder ID: {folder.get('id')}")

            return folder.get('id')

        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def search_files(self, query):
        """
        Search for files in Google Drive

        Args:
            query: Search query string
                   Examples:
                   - "name contains 'report'"
                   - "mimeType='application/pdf'"
                   - "fullText contains 'important'"

        Returns:
            List of matching files
        """
        return self.list_files(page_size=50, query=query)


def main():
    """Example usage"""
    print("Google Drive API - Authentication and Basic Operations\n")

    # Initialize the API
    drive = GoogleDriveAPI()

    # List recent files
    print("\n" + "="*60)
    print("Listing 10 most recent files:")
    print("="*60)
    drive.list_files(page_size=10)

    # Example: Search for specific files
    print("\n" + "="*60)
    print("Searching for PDF files:")
    print("="*60)
    drive.search_files("mimeType='application/pdf'")


if __name__ == '__main__':
    main()
