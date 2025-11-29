#!/usr/bin/env python3
"""
Data analysis example for iSH
Demonstrates basic data manipulation with lists and dictionaries
"""

import json
from datetime import datetime
from collections import Counter

# Sample data
SAMPLE_DATA = [
    {"name": "Alice", "age": 25, "city": "New York", "score": 85},
    {"name": "Bob", "age": 30, "city": "San Francisco", "score": 92},
    {"name": "Charlie", "age": 25, "city": "New York", "score": 78},
    {"name": "David", "age": 35, "city": "Boston", "score": 88},
    {"name": "Eve", "age": 30, "city": "San Francisco", "score": 95},
]

def display_data():
    """Display the data in a formatted table"""
    print("\n📊 Sample Data:")
    print("-" * 60)
    print(f"{'Name':<12} {'Age':<6} {'City':<20} {'Score':<6}")
    print("-" * 60)
    for item in SAMPLE_DATA:
        print(f"{item['name']:<12} {item['age']:<6} {item['city']:<20} {item['score']:<6}")
    print("-" * 60)

def analyze_data():
    """Perform basic analysis"""
    print("\n📈 Data Analysis:")

    # Calculate average age
    avg_age = sum(item['age'] for item in SAMPLE_DATA) / len(SAMPLE_DATA)
    print(f"  Average age: {avg_age:.1f}")

    # Calculate average score
    avg_score = sum(item['score'] for item in SAMPLE_DATA) / len(SAMPLE_DATA)
    print(f"  Average score: {avg_score:.1f}")

    # Count by city
    cities = Counter(item['city'] for item in SAMPLE_DATA)
    print(f"\n  People by city:")
    for city, count in cities.most_common():
        print(f"    {city}: {count}")

    # Find highest score
    highest = max(SAMPLE_DATA, key=lambda x: x['score'])
    print(f"\n  Highest score: {highest['name']} with {highest['score']}")

def filter_data():
    """Filter data based on criteria"""
    print("\n🔍 Filter Data:")
    min_score = int(input("  Minimum score: ").strip() or "0")

    filtered = [item for item in SAMPLE_DATA if item['score'] >= min_score]

    print(f"\n  Found {len(filtered)} people with score >= {min_score}:")
    for item in filtered:
        print(f"    {item['name']}: {item['score']}")

def add_person():
    """Add a new person to the data"""
    print("\n➕ Add New Person:")
    name = input("  Name: ").strip()
    age = int(input("  Age: ").strip())
    city = input("  City: ").strip()
    score = int(input("  Score: ").strip())

    SAMPLE_DATA.append({
        "name": name,
        "age": age,
        "city": city,
        "score": score
    })
    print(f"✅ Added {name} to the data!")

def save_to_file():
    """Save data to JSON file"""
    filename = "data.json"
    with open(filename, "w") as f:
        json.dump(SAMPLE_DATA, f, indent=2)
    print(f"✅ Data saved to {filename}")

def main():
    print("=" * 60)
    print("  📊 Data Analysis Demo")
    print("=" * 60)

    while True:
        print("\nChoose an option:")
        print("  1. Display data")
        print("  2. Analyze data")
        print("  3. Filter data")
        print("  4. Add person")
        print("  5. Save to file")
        print("  6. Exit")

        choice = input("\nYour choice (1-6): ").strip()

        if choice == "1":
            display_data()
        elif choice == "2":
            analyze_data()
        elif choice == "3":
            filter_data()
        elif choice == "4":
            add_person()
        elif choice == "5":
            save_to_file()
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
