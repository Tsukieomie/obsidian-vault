#!/usr/bin/env python3
"""
Example Usage Script - Google Drive & YouTube APIs

This script demonstrates how to use both Google Drive and YouTube APIs together.
It shows practical examples of common use cases.

Requirements:
    pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
"""

import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google_drive_auth import GoogleDriveAPI
from youtube_api_auth import YouTubeAPI


def example_1_basic_authentication():
    """Example 1: Basic authentication with both APIs"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Authentication")
    print("="*70)

    # Initialize both APIs
    print("\n1. Authenticating with Google Drive...")
    drive = GoogleDriveAPI()

    print("\n2. Authenticating with YouTube...")
    youtube = YouTubeAPI()

    print("\n✓ Successfully authenticated with both APIs!")
    return drive, youtube


def example_2_drive_operations(drive):
    """Example 2: Common Google Drive operations"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Google Drive Operations")
    print("="*70)

    # List recent files
    print("\n1. Listing your 5 most recent files:")
    drive.list_files(page_size=5)

    # Search for specific file types
    print("\n2. Searching for documents:")
    docs = drive.search_files("mimeType='application/vnd.google-apps.document'")

    print("\n3. Searching for images:")
    images = drive.search_files("mimeType contains 'image/'")


def example_3_youtube_operations(youtube):
    """Example 3: Common YouTube operations"""
    print("\n" + "="*70)
    print("EXAMPLE 3: YouTube Operations")
    print("="*70)

    # Get your channel info
    print("\n1. Getting your channel information:")
    channel = youtube.get_my_channel()

    # Search for videos
    print("\n2. Searching for videos about 'machine learning':")
    videos = youtube.search_videos("machine learning", max_results=3)

    # Get your playlists
    print("\n3. Getting your playlists:")
    playlists = youtube.get_my_playlists()


def example_4_combined_workflow(drive, youtube):
    """Example 4: Combined workflow - Save YouTube data to Drive"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Combined Workflow")
    print("="*70)
    print("This example shows how to combine both APIs")

    # Get YouTube channel info
    print("\n1. Fetching your YouTube channel data...")
    channel = youtube.get_my_channel()

    if channel:
        # Create a report file
        report_path = "/tmp/youtube_channel_report.txt"

        print("\n2. Creating channel report...")
        with open(report_path, 'w') as f:
            f.write("YouTube Channel Report\n")
            f.write("="*50 + "\n\n")
            f.write(f"Channel Name: {channel['snippet']['title']}\n")
            f.write(f"Channel ID: {channel['id']}\n")
            f.write(f"Subscribers: {channel['statistics'].get('subscriberCount', 'Hidden')}\n")
            f.write(f"Total Views: {channel['statistics']['viewCount']}\n")
            f.write(f"Total Videos: {channel['statistics']['videoCount']}\n")
            f.write(f"\nDescription:\n{channel['snippet']['description']}\n")

        print(f"✓ Report created at: {report_path}")

        # Upload to Google Drive
        print("\n3. Uploading report to Google Drive...")
        file_id = drive.upload_file(report_path)

        if file_id:
            print("✓ Report successfully uploaded to Google Drive!")

        # Clean up
        os.remove(report_path)


def example_5_video_analysis(youtube):
    """Example 5: Analyze a specific video"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Video Analysis")
    print("="*70)

    # Search for a video
    print("\n1. Searching for Python tutorial videos...")
    videos = youtube.search_videos("Python tutorial for beginners", max_results=1)

    if videos and len(videos) > 0:
        video_id = videos[0]['id']['videoId']

        # Get detailed info
        print("\n2. Getting detailed information...")
        video_details = youtube.get_video_details(video_id)

        # Get comments
        print("\n3. Getting comments...")
        comments = youtube.get_video_comments(video_id, max_results=5)


def example_6_playlist_backup(drive, youtube):
    """Example 6: Backup YouTube playlist data to Drive"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Playlist Backup to Drive")
    print("="*70)

    # Get playlists
    print("\n1. Fetching your playlists...")
    playlists = youtube.get_my_playlists()

    if playlists and len(playlists) > 0:
        # Create backup file
        backup_path = "/tmp/youtube_playlists_backup.txt"

        print("\n2. Creating playlist backup...")
        with open(backup_path, 'w') as f:
            f.write("YouTube Playlists Backup\n")
            f.write("="*50 + "\n\n")

            for playlist in playlists:
                f.write(f"\nPlaylist: {playlist['snippet']['title']}\n")
                f.write(f"ID: {playlist['id']}\n")
                f.write(f"Videos: {playlist['contentDetails']['itemCount']}\n")
                f.write(f"Description: {playlist['snippet']['description'][:200]}\n")
                f.write("-"*50 + "\n")

        print(f"✓ Backup created at: {backup_path}")

        # Upload to Drive
        print("\n3. Uploading backup to Google Drive...")
        file_id = drive.upload_file(backup_path)

        if file_id:
            print("✓ Backup successfully uploaded to Google Drive!")

        # Clean up
        os.remove(backup_path)


def main():
    """Main function to run all examples"""
    print("\n" + "="*70)
    print("GOOGLE DRIVE & YOUTUBE API - EXAMPLE USAGE")
    print("="*70)
    print("\nThis script demonstrates various use cases for both APIs.")
    print("You will be prompted to authenticate with Google in your browser.")

    try:
        # Example 1: Authentication
        drive, youtube = example_1_basic_authentication()

        # Example 2: Drive operations
        example_2_drive_operations(drive)

        # Example 3: YouTube operations
        example_3_youtube_operations(youtube)

        # Example 4: Combined workflow
        example_4_combined_workflow(drive, youtube)

        # Example 5: Video analysis
        example_5_video_analysis(youtube)

        # Example 6: Playlist backup
        example_6_playlist_backup(drive, youtube)

        print("\n" + "="*70)
        print("✓ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*70)

    except Exception as e:
        print(f"\n✗ An error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
