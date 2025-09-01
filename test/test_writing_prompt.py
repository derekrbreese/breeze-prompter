#!/usr/bin/env python3
import requests
import json

# Test the API with a writing prompt
url = "http://localhost:8002/api/perfect-prompt"

test_data = {
    "prompt": "write a blog post about AI",
    "context": "writing",
    "style": "detailed",
    "include_examples": False
}

response = requests.post(url, json=test_data)

if response.status_code == 200:
    result = response.json()
    print("✅ Writing Prompt Test Successful!\n")
    print("=" * 60)
    print("ORIGINAL PROMPT:")
    print(f"  {result['original_prompt']}\n")
    print("ENHANCED PROMPT:")
    print(f"  {result['enhanced_prompt']}\n")
    print("EXPLANATION:")
    print(f"  {result['explanation']}\n")
    print("SCORES:")
    print(f"  Before: Overall={result['score_before']['overall']}")
    print(f"  After:  Overall={result['score_after']['overall']}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)