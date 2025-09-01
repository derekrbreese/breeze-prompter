#!/usr/bin/env python3
import requests
import json

# Test different complexity levels
url = "http://localhost:8002/api/gpt-enhance"

test_cases = [
    # Simple queries (shouldn't get heavy role assignment)
    {
        "name": "Simple Question",
        "prompt": "What's the capital of France?",
        "context": "general"
    },
    {
        "name": "Simple Calculation",
        "prompt": "Calculate 15% tip on $45",
        "context": "general"
    },
    {
        "name": "Simple List",
        "prompt": "List 5 healthy breakfast options",
        "context": "general"
    },
    # Moderate complexity (might get role if beneficial)
    {
        "name": "Moderate Coding",
        "prompt": "Write a function to reverse a string",
        "context": "coding"
    },
    # Complex tasks (should get full treatment)
    {
        "name": "Complex Development",
        "prompt": "Build a real-time chat application with user authentication",
        "context": "coding"
    },
    {
        "name": "Complex Analysis",
        "prompt": "Analyze customer behavior patterns from our Q4 sales data to identify opportunities for revenue growth",
        "context": "analysis"
    }
]

for test in test_cases:
    print(f"\n{'='*60}")
    print(f"TEST: {test['name']}")
    print(f"Prompt: {test['prompt']}")
    print(f"{'='*60}")
    
    response = requests.post(url, json={
        "prompt": test["prompt"],
        "context": test["context"]
    })
    
    if response.status_code == 200:
        result = response.json()
        enhanced = result['enhanced_prompt']
        
        # Check for role establishment
        has_role = "You are" in enhanced or "### Instruction" in enhanced
        
        print(f"✅ Enhanced successfully")
        print(f"Has Role/Scaffolding: {has_role}")
        print(f"\nFirst 300 chars of enhancement:")
        print(enhanced[:300] + "..." if len(enhanced) > 300 else enhanced)
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)