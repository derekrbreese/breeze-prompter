#!/usr/bin/env python3
import requests
import json

# Test the API with a sample prompt
url = "http://localhost:8002/api/perfect-prompt"

test_data = {
    "prompt": "write code for sorting",
    "context": "coding",
    "style": "detailed",
    "include_examples": True
}

response = requests.post(url, json=test_data)

if response.status_code == 200:
    result = response.json()
    print("✅ API Test Successful!\n")
    print("=" * 60)
    print("ORIGINAL PROMPT:")
    print(f"  {result['original_prompt']}\n")
    print("ENHANCED PROMPT:")
    print(f"  {result['enhanced_prompt']}\n")
    print("IMPROVEMENTS:")
    for imp in result['improvements']:
        print(f"  • [{imp['category']}] {imp['description']}")
    print("\nEXPLANATION:")
    print(f"  {result['explanation']}\n")
    print("SCORES:")
    print(f"  Before: Clarity={result['score_before']['clarity']}, "
          f"Specificity={result['score_before']['specificity']}, "
          f"Overall={result['score_before']['overall']}")
    print(f"  After:  Clarity={result['score_after']['clarity']}, "
          f"Specificity={result['score_after']['specificity']}, "
          f"Overall={result['score_after']['overall']}")
    if result.get('tips'):
        print("\nTIPS:")
        for tip in result['tips']:
            print(f"  • {tip}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)