#!/usr/bin/env python3
"""
Web fetching example for iSH
Demonstrates making HTTP requests
"""

try:
    import requests
except ImportError:
    print("❌ 'requests' package not installed!")
    print("Run: pip3 install requests")
    exit(1)

import json

def fetch_url(url):
    """Fetch content from a URL"""
    try:
        print(f"🌐 Fetching {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        print(f"✅ Status: {response.status_code}")
        print(f"📦 Size: {len(response.content)} bytes")

        return response
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None

def fetch_json_api():
    """Fetch JSON data from a public API"""
    url = "https://api.github.com/users/github"
    response = fetch_url(url)

    if response:
        data = response.json()
        print("\n📊 GitHub User Data:")
        print(f"  Name: {data.get('name')}")
        print(f"  Bio: {data.get('bio')}")
        print(f"  Public Repos: {data.get('public_repos')}")
        print(f"  Followers: {data.get('followers')}")

def download_file(url, filename):
    """Download a file from URL"""
    try:
        print(f"⬇️  Downloading {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(filename, 'wb') as f:
            f.write(response.content)

        print(f"✅ Saved to {filename}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("=" * 50)
    print("  🌐 Web Fetching Demo")
    print("=" * 50)

    while True:
        print("\nChoose an option:")
        print("  1. Fetch a URL")
        print("  2. Fetch GitHub API example")
        print("  3. Download a file")
        print("  4. Exit")

        choice = input("\nYour choice (1-4): ").strip()

        if choice == "1":
            url = input("Enter URL: ").strip()
            response = fetch_url(url)
            if response:
                print(f"\n📄 First 500 characters:")
                print(response.text[:500])

        elif choice == "2":
            fetch_json_api()

        elif choice == "3":
            url = input("Enter file URL: ").strip()
            filename = input("Save as: ").strip()
            download_file(url, filename)

        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
