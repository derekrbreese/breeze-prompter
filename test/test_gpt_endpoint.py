#!/usr/bin/env python3
import requests
import json

# Test the new GPT endpoint
url = "http://localhost:8002/api/gpt-enhance"

# Test 1: Simple prompt without document context
test1 = {
    "prompt": "write a function to calculate fibonacci numbers",
    "context": "coding",
    "style": "detailed"
}

print("=" * 60)
print("TEST 1: Simple prompt without document context")
print("=" * 60)
response = requests.post(url, json=test1)
if response.status_code == 200:
    result = response.json()
    print("✅ Success!")
    print("\nEnhanced Prompt:")
    print(result['enhanced_prompt'])
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

# Test 2: Prompt with document context
test2 = {
    "prompt": "summarize the key points",
    "document_context": """
    Recent Quarterly Report:
    - Revenue increased by 25% YoY to $145M
    - Customer acquisition cost decreased by 15%
    - New product launch scheduled for Q2
    - Market expansion into 3 new regions
    - Employee headcount grew by 40 people
    """,
    "context": "analysis",
    "style": "concise"
}

print("\n" + "=" * 60)
print("TEST 2: Prompt with document context")
print("=" * 60)
response = requests.post(url, json=test2)
if response.status_code == 200:
    result = response.json()
    print("✅ Success!")
    print("\nEnhanced Prompt:")
    print(result['enhanced_prompt'])
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

# Test 3: Time-sensitive query with current info
test3 = {
    "prompt": "what are the latest AI developments",
    "context": "technical",
    "fetch_current_info": True
}

print("\n" + "=" * 60)
print("TEST 3: Time-sensitive query with current info")
print("=" * 60)
response = requests.post(url, json=test3)
if response.status_code == 200:
    result = response.json()
    print("✅ Success!")
    print("\nEnhanced Prompt (should include current info):")
    print(result['enhanced_prompt'][:500] + "..." if len(result['enhanced_prompt']) > 500 else result['enhanced_prompt'])
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)