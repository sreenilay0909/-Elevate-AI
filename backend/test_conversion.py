"""Test the camelCase conversion function"""
from app.schemas.platform_schemas import convert_dict_keys_to_camel
import json

# Test data from database (snake_case)
test_data = {
    "github": {
        "repositories": 19,
        "stars": 0,
        "commits_last_year": 340,
        "top_languages": ["JavaScript", "HTML", "Python"],
        "contribution_streak": 357,
        "followers": 9,
        "following": 12
    },
    "leetcode": {
        "total_solved": 119,
        "easy_solved": 80,
        "medium_solved": 37,
        "hard_solved": 2,
        "acceptance_rate": 54.3,
        "ranking": 1240776,
        "streak": 20
    },
    "geeksforgeeks": {
        "coding_score": 0,
        "problems_solved": 0,
        "practice_streak": 0,
        "institute_rank": 0,
        "monthly_score": 0
    }
}

print("=== Testing camelCase Conversion ===\n")

for platform, data in test_data.items():
    print(f"\n{platform.upper()}:")
    print(f"Before: {json.dumps(data, indent=2)}")
    
    converted = convert_dict_keys_to_camel(data)
    print(f"\nAfter: {json.dumps(converted, indent=2)}")
    print("-" * 60)
