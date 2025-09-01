#!/usr/bin/env python3
import requests
import json

# Test the API with intentionally vague prompts
url = "http://localhost:8002/api/perfect-prompt"

vague_prompts = [
    {
        "prompt": "make it better",
        "context": "general",
        "style": "detailed"
    },
    {
        "prompt": "help me with the thing",
        "context": "technical",
        "style": "concise"
    },
    {
        "prompt": "do the analysis",
        "context": "analysis",
        "style": "detailed"
    }
]

for i, test_data in enumerate(vague_prompts, 1):
    print(f"\n{'='*60}")
    print(f"TEST {i}: Testing vague prompt")
    print(f"{'='*60}")
    
    response = requests.post(url, json=test_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nORIGINAL: {result['original_prompt']}")
        print(f"\nENHANCED:\n{result['enhanced_prompt'][:500]}..." if len(result['enhanced_prompt']) > 500 else f"\nENHANCED:\n{result['enhanced_prompt']}")
        print(f"\nSCORE IMPROVEMENT: {result['score_before']['overall']} → {result['score_after']['overall']}")
        print(f"\nEXPLANATION: {result['explanation']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)