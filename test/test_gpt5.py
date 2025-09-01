#!/usr/bin/env python3
import requests
import json

# Test GPT-5 optimized prompt enhancement
url = "http://localhost:8002/api/perfect-prompt"

test_cases = [
    {
        "name": "Coding Task",
        "data": {
            "prompt": "build a web scraper",
            "context": "coding",
            "style": "detailed",
            "include_examples": True
        }
    },
    {
        "name": "Analysis Task",
        "data": {
            "prompt": "analyze customer feedback",
            "context": "analysis",
            "style": "technical",
            "include_examples": False
        }
    },
    {
        "name": "Creative Task",
        "data": {
            "prompt": "create a marketing campaign",
            "context": "creative",
            "style": "detailed",
            "include_examples": True
        }
    }
]

for test in test_cases:
    print(f"\n{'='*70}")
    print(f"Testing GPT-5 Optimization: {test['name']}")
    print(f"{'='*70}")
    
    response = requests.post(url, json=test['data'])
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\nORIGINAL: {result['original_prompt']}")
        print(f"\nENHANCED (First 800 chars):")
        enhanced = result['enhanced_prompt']
        print(enhanced[:800] + "..." if len(enhanced) > 800 else enhanced)
        
        print(f"\nGPT-5 OPTIMIZATION FEATURES:")
        # Check for GPT-5 specific patterns
        features = []
        if "###" in enhanced:
            features.append("✓ Structured scaffolding with ### markers")
        if "<<<" in enhanced and ">>>" in enhanced:
            features.append("✓ Input delimiters for injection resistance")
        if "Knowledge Cutoff" in enhanced or "Current Date" in enhanced:
            features.append("✓ Temporal anchoring")
        if "reasoning_effort" in enhanced.lower() or "step-by-step" in enhanced.lower():
            features.append("✓ Explicit reasoning chains")
        if "confidence" in enhanced.lower():
            features.append("✓ Confidence scoring requirement")
        if "Primary" in enhanced and "Secondary" in enhanced:
            features.append("✓ Context hierarchy")
        if "success criteria" in enhanced.lower() or "evaluation" in enhanced.lower():
            features.append("✓ Evaluation-first design")
            
        for feature in features:
            print(f"  {feature}")
            
        print(f"\nSCORE: {result['score_before']['overall']} → {result['score_after']['overall']}")
        print(f"EXPLANATION: {result['explanation']}")
        
        if result.get('tips'):
            print("\nGPT-5 TIPS:")
            for tip in result['tips'][:3]:
                print(f"  • {tip}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)