#!/usr/bin/env python3
"""
YouTube Data API Authentication and Access Script

This script authenticates with YouTube Data API using OAuth 2.0 and provides
functionality to interact with YouTube channels, videos, playlists, and comments.

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

# Define the scopes for YouTube Data API
# For read-only access, use 'https://www.googleapis.com/auth/youtube.readonly'
# For full access (read/write), use 'https://www.googleapis.com/auth/youtube'
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(SCRIPT_DIR, 'youtube_token.pickle')


class YouTubeAPI:
    """YouTube Data API wrapper class"""

    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with YouTube Data API"""
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
        self.service = build('youtube', 'v3', credentials=self.creds)
        print("✓ Successfully authenticated with YouTube Data API")

    def get_my_channel(self):
        """Get information about the authenticated user's channel"""
        try:
            request = self.service.channels().list(
                part='snippet,contentDetails,statistics',
                mine=True
            )
            response = request.execute()

            if 'items' in response and len(response['items']) > 0:
                channel = response['items'][0]
                print("\n" + "="*60)
                print("YOUR CHANNEL INFORMATION")
                print("="*60)
                print(f"Channel Name: {channel['snippet']['title']}")
                print(f"Channel ID: {channel['id']}")
                print(f"Subscribers: {channel['statistics'].get('subscriberCount', 'Hidden')}")
                print(f"Total Views: {channel['statistics']['viewCount']}")
                print(f"Total Videos: {channel['statistics']['videoCount']}")
                print(f"Description: {channel['snippet']['description'][:100]}...")
                return channel
            else:
                print("No channel found for this account.")
                return None

        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def search_videos(self, query, max_results=10):
        """
        Search for videos on YouTube

        Args:
            query: Search query string
            max_results: Maximum number of results to return (default: 10)

        Returns:
            List of video items
        """
        try:
            request = self.service.search().list(
                part='snippet',
                q=query,
                type='video',
                maxResults=max_results
            )
            response = request.execute()

            videos = response.get('items', [])

            print(f"\n✓ Found {len(videos)} videos for query: '{query}'")
            for idx, video in enumerate(videos, 1):
                print(f"\n{idx}. {video['snippet']['title']}")
                print(f"   Channel: {video['snippet']['channelTitle']}")
                print(f"   Video ID: {video['id']['videoId']}")
                print(f"   URL: https://www.youtube.com/watch?v={video['id']['videoId']}")

            return videos

        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def get_video_details(self, video_id):
        """
        Get detailed information about a specific video

        Args:
            video_id: YouTube video ID

        Returns:
            Video details dictionary
        """
        try:
            request = self.service.videos().list(
                part='snippet,contentDetails,statistics',
                id=video_id
            )
            response = request.execute()

            if 'items' in response and len(response['items']) > 0:
                video = response['items'][0]
                print("\n" + "="*60)
                print(f"VIDEO DETAILS: {video['snippet']['title']}")
                print("="*60)
                print(f"Channel: {video['snippet']['channelTitle']}")
                print(f"Published: {video['snippet']['publishedAt']}")
                print(f"Views: {video['statistics'].get('viewCount', 'N/A')}")
                print(f"Likes: {video['statistics'].get('likeCount', 'N/A')}")
                print(f"Comments: {video['statistics'].get('commentCount', 'N/A')}")
                print(f"Duration: {video['contentDetails']['duration']}")
                print(f"\nDescription:\n{video['snippet']['description'][:300]}...")
                return video
            else:
                print(f"Video not found: {video_id}")
                return None

        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def get_playlist_videos(self, playlist_id, max_results=50):
        """
        Get videos from a playlist

        Args:
            playlist_id: YouTube playlist ID
            max_results: Maximum number of videos to retrieve (default: 50)

        Returns:
            List of video items in the playlist
        """
        try:
            videos = []
            next_page_token = None

            while len(videos) < max_results:
                request = self.service.playlistItems().list(
                    part='snippet,contentDetails',
                    playlistId=playlist_id,
                    maxResults=min(50, max_results - len(videos)),
                    pageToken=next_page_token
                )
                response = request.execute()

                videos.extend(response.get('items', []))
                next_page_token = response.get('nextPageToken')

                if not next_page_token:
                    break

            print(f"\n✓ Retrieved {len(videos)} videos from playlist")
            for idx, video in enumerate(videos[:10], 1):  # Show first 10
                print(f"{idx}. {video['snippet']['title']}")

            return videos

        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def get_video_comments(self, video_id, max_results=20):
        """
        Get comments from a video

        Args:
            video_id: YouTube video ID
            max_results: Maximum number of comments to retrieve (default: 20)

        Returns:
            List of comment items
        """
        try:
            request = self.service.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=max_results,
                textFormat='plainText'
            )
            response = request.execute()

            comments = response.get('items', [])

            print(f"\n✓ Retrieved {len(comments)} comments")
            for idx, comment in enumerate(comments[:10], 1):  # Show first 10
                top_comment = comment['snippet']['topLevelComment']['snippet']
                print(f"\n{idx}. {top_comment['authorDisplayName']}")
                print(f"   {top_comment['textDisplay'][:100]}...")
                print(f"   Likes: {top_comment['likeCount']}")

            return comments

        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def get_channel_videos(self, channel_id, max_results=10):
        """
        Get recent videos from a specific channel

        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of videos to retrieve (default: 10)

        Returns:
            List of video items
        """
        try:
            request = self.service.search().list(
                part='snippet',
                channelId=channel_id,
                type='video',
                order='date',
                maxResults=max_results
            )
            response = request.execute()

            videos = response.get('items', [])

            print(f"\n✓ Retrieved {len(videos)} videos from channel")
            for idx, video in enumerate(videos, 1):
                print(f"{idx}. {video['snippet']['title']}")
                print(f"   Published: {video['snippet']['publishedAt']}")

            return videos

        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def get_my_playlists(self):
        """Get playlists from the authenticated user's channel"""
        try:
            request = self.service.playlists().list(
                part='snippet,contentDetails',
                mine=True,
                maxResults=25
            )
            response = request.execute()

            playlists = response.get('items', [])

            print(f"\n✓ Found {len(playlists)} playlists")
            for idx, playlist in enumerate(playlists, 1):
                print(f"{idx}. {playlist['snippet']['title']}")
                print(f"   ID: {playlist['id']}")
                print(f"   Videos: {playlist['contentDetails']['itemCount']}")

            return playlists

        except HttpError as error:
            print(f'An error occurred: {error}')
            return []


def main():
    """Example usage"""
    print("YouTube Data API - Authentication and Basic Operations\n")

    # Initialize the API
    youtube = YouTubeAPI()

    # Get authenticated user's channel info
    youtube.get_my_channel()

    # Search for videos
    print("\n" + "="*60)
    print("Searching for videos about 'Python programming':")
    print("="*60)
    youtube.search_videos("Python programming", max_results=5)

    # Get playlists (if the user has any)
    print("\n" + "="*60)
    print("Your playlists:")
    print("="*60)
    youtube.get_my_playlists()


if __name__ == '__main__':
    main()
