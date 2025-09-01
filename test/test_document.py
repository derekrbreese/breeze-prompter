#!/usr/bin/env python3
import requests
import json

# Test document context handling
url = "http://localhost:8002/api/gpt-enhance"

# Test with document context
test = {
    "prompt": "improve this text",
    "document_context": """
    Our company has been growing rapidly over the past year. 
    We've expanded from 50 to 200 employees and opened three new offices.
    Revenue has increased by 150% and we've launched 5 new products.
    However, we're facing challenges with scaling our operations.
    """,
    "context": "writing"
}

print("Testing Document Context Enhancement")
print("=" * 60)
print(f"User prompt: {test['prompt']}")
print(f"Document: {test['document_context'][:100]}...")
print("=" * 60)

response = requests.post(url, json=test, timeout=30)

if response.status_code == 200:
    result = response.json()
    enhanced = result['enhanced_prompt']
    
    print("✅ Success!")
    print("\nEnhanced Prompt:")
    print(enhanced)
    
    # Check for problematic patterns
    problems = []
    if "<<<" in enhanced:
        problems.append("Contains placeholder tags")
    if "### Instruction" in enhanced:
        problems.append("Contains complex scaffolding")
    if "### Context" in enhanced:
        problems.append("Contains multiple sections")
    
    if problems:
        print("\n⚠️  Issues found:")
        for p in problems:
            print(f"  - {p}")
    else:
        print("\n✅ Clean, natural enhancement!")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)