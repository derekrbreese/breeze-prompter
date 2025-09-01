#!/usr/bin/env python3
import requests
import time

url = "http://localhost:8002/api/gpt-enhance"

test_cases = [
    ("Simple", "What's the capital of France?"),
    ("Moderate", "Write a Python function to reverse a string"),
    ("Complex", "Build a real-time chat application with user authentication and message persistence")
]

print("Performance Test Results")
print("=" * 60)

for complexity, prompt in test_cases:
    test = {
        "prompt": prompt,
        "context": "general"
    }
    
    print(f"\n{complexity} Prompt: {prompt[:40]}...")
    start = time.time()
    
    try:
        response = requests.post(url, json=test, timeout=70)
        
        if response.status_code == 200:
            elapsed = time.time() - start
            result = response.json()
            print(f"✅ Success in {elapsed:.1f} seconds")
            print(f"   Response length: {len(result['enhanced_prompt'])} chars")
        else:
            print(f"❌ Error: {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"❌ Timeout after 70 seconds")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 60)