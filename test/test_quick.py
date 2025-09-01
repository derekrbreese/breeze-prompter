#!/usr/bin/env python3
import requests
import time

# Quick test with a simple prompt
url = "http://localhost:8002/api/gpt-enhance"

test = {
    "prompt": "What's 2+2?",
    "context": "general"
}

print("Testing simple prompt...")
start = time.time()
response = requests.post(url, json=test, timeout=70)  # 70 second timeout

if response.status_code == 200:
    elapsed = time.time() - start
    result = response.json()
    print(f"✅ Success in {elapsed:.1f} seconds")
    print(f"Response length: {len(result['enhanced_prompt'])} chars")
    print(f"First 200 chars: {result['enhanced_prompt'][:200]}...")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)