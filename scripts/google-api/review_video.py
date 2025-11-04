#!/usr/bin/env python3
"""
Video Review Script - Analyzes a specific YouTube video
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from youtube_api_auth import YouTubeAPI


def parse_duration(duration):
    """Convert ISO 8601 duration to readable format"""
    import re
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(duration)
    if not match:
        return "Unknown"

    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0:
        parts.append(f"{seconds}s")

    return " ".join(parts) if parts else "0s"


def format_number(num):
    """Format large numbers with commas"""
    try:
        return f"{int(num):,}"
    except:
        return str(num)


def analyze_video(video_id):
    """Comprehensive video analysis"""
    print("="*70)
    print("YOUTUBE VIDEO REVIEW")
    print("="*70)
    print(f"\nVideo ID: {video_id}")
    print(f"URL: https://www.youtube.com/watch?v={video_id}\n")

    # Initialize YouTube API
    youtube = YouTubeAPI()

    # Get video details
    print("Fetching video details...")
    video = youtube.get_video_details(video_id)

    if not video:
        print("ERROR: Could not retrieve video information.")
        return None

    # Extract data
    snippet = video['snippet']
    statistics = video['statistics']
    content_details = video['contentDetails']

    # Basic Info
    print("\n" + "="*70)
    print("BASIC INFORMATION")
    print("="*70)
    print(f"Title: {snippet['title']}")
    print(f"Channel: {snippet['channelTitle']}")
    print(f"Channel ID: {snippet['channelId']}")
    print(f"Published: {snippet['publishedAt']}")
    print(f"Duration: {parse_duration(content_details['duration'])}")

    # Statistics
    print("\n" + "="*70)
    print("STATISTICS")
    print("="*70)
    print(f"Views: {format_number(statistics.get('viewCount', 'N/A'))}")
    print(f"Likes: {format_number(statistics.get('likeCount', 'N/A'))}")
    print(f"Comments: {format_number(statistics.get('commentCount', 'N/A'))}")

    # Calculate engagement metrics
    views = int(statistics.get('viewCount', 0))
    likes = int(statistics.get('likeCount', 0))
    comments = int(statistics.get('commentCount', 0))

    if views > 0:
        like_ratio = (likes / views) * 100
        comment_ratio = (comments / views) * 100
        print(f"\nEngagement Rate:")
        print(f"  Like Ratio: {like_ratio:.2f}%")
        print(f"  Comment Ratio: {comment_ratio:.2f}%")

    # Description
    print("\n" + "="*70)
    print("DESCRIPTION")
    print("="*70)
    description = snippet['description']
    if len(description) > 500:
        print(description[:500] + "...\n[truncated]")
    else:
        print(description)

    # Tags
    if 'tags' in snippet:
        print("\n" + "="*70)
        print("TAGS")
        print("="*70)
        tags = snippet['tags'][:20]  # Show first 20 tags
        print(", ".join(tags))

    # Category
    category_id = snippet.get('categoryId', 'Unknown')
    categories = {
        '1': 'Film & Animation', '2': 'Autos & Vehicles',
        '10': 'Music', '15': 'Pets & Animals',
        '17': 'Sports', '19': 'Travel & Events',
        '20': 'Gaming', '22': 'People & Blogs',
        '23': 'Comedy', '24': 'Entertainment',
        '25': 'News & Politics', '26': 'Howto & Style',
        '27': 'Education', '28': 'Science & Technology',
        '29': 'Nonprofits & Activism'
    }
    category_name = categories.get(category_id, 'Unknown')
    print(f"\nCategory: {category_name}")

    # Get comments
    print("\n" + "="*70)
    print("TOP COMMENTS")
    print("="*70)

    try:
        comments_list = youtube.get_video_comments(video_id, max_results=10)

        if comments_list:
            for idx, comment in enumerate(comments_list[:5], 1):
                top_comment = comment['snippet']['topLevelComment']['snippet']
                print(f"\n{idx}. {top_comment['authorDisplayName']}")
                print(f"   Likes: {top_comment['likeCount']}")
                text = top_comment['textDisplay']
                if len(text) > 200:
                    text = text[:200] + "..."
                print(f"   \"{text}\"")
        else:
            print("No comments available or comments are disabled.")
    except Exception as e:
        print(f"Could not fetch comments: {e}")

    # Get channel info
    print("\n" + "="*70)
    print("CHANNEL INFORMATION")
    print("="*70)

    try:
        channel_videos = youtube.get_channel_videos(snippet['channelId'], max_results=5)
        if channel_videos:
            print(f"\nRecent videos from {snippet['channelTitle']}:")
            for idx, vid in enumerate(channel_videos[:5], 1):
                print(f"{idx}. {vid['snippet']['title']}")
    except Exception as e:
        print(f"Could not fetch channel videos: {e}")

    # Summary
    print("\n" + "="*70)
    print("REVIEW SUMMARY")
    print("="*70)

    # Engagement analysis
    if views > 0:
        if like_ratio > 5:
            engagement = "Excellent"
        elif like_ratio > 2:
            engagement = "Good"
        elif like_ratio > 1:
            engagement = "Average"
        else:
            engagement = "Low"

        print(f"\nEngagement Level: {engagement}")
        print(f"The video has a {like_ratio:.2f}% like ratio, which is considered {engagement.lower()}.")

    # Popularity analysis
    if views > 1000000:
        popularity = "Viral"
    elif views > 100000:
        popularity = "Very Popular"
    elif views > 10000:
        popularity = "Popular"
    elif views > 1000:
        popularity = "Moderate"
    else:
        popularity = "Low visibility"

    print(f"\nPopularity: {popularity}")
    print(f"With {format_number(views)} views, this video has {popularity.lower()} reach.")

    # Save report
    report_path = f"/tmp/video_review_{video_id}.json"
    with open(report_path, 'w') as f:
        json.dump({
            'video_id': video_id,
            'title': snippet['title'],
            'channel': snippet['channelTitle'],
            'published': snippet['publishedAt'],
            'views': views,
            'likes': likes,
            'comments': comments,
            'like_ratio': like_ratio if views > 0 else 0,
            'engagement': engagement if views > 0 else 'N/A',
            'popularity': popularity,
            'category': category_name,
            'duration': parse_duration(content_details['duration']),
            'description': description[:500]
        }, f, indent=2)

    print(f"\n✓ Full report saved to: {report_path}")

    return video


if __name__ == '__main__':
    # Video ID from URL: https://m.youtube.com/watch?v=N02SK9yd60s
    VIDEO_ID = "N02SK9yd60s"

    analyze_video(VIDEO_ID)
