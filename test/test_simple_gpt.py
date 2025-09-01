#!/usr/bin/env python3
import requests
import json

# Test the new GPT endpoint with a simple request
url = "http://localhost:8002/api/gpt-enhance"

# Simple test that should return quickly
test = {
    "prompt": "help me write better code",
    "context": "coding"
}

print("Testing GPT endpoint...")
response = requests.post(url, json=test)

if response.status_code == 200:
    result = response.json()
    print("✅ Success!")
    print("\nResponse structure:", json.dumps(result, indent=2))
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)