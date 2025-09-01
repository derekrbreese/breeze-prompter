#!/usr/bin/env python3
import requests
import json

# Test knowledge-enhanced prompt generation
url = "http://localhost:8002/api/perfect-prompt"

test_cases = [
    {
        "name": "Time-Sensitive Technical Query",
        "data": {
            "prompt": "how to use the latest GPT-5 features",
            "context": "technical",
            "style": "detailed",
            "include_examples": True,
            "fetch_current_knowledge": True  # Enable knowledge fetching
        }
    },
    {
        "name": "Current Best Practices",
        "data": {
            "prompt": "implement modern React patterns in 2025",
            "context": "coding",
            "style": "technical",
            "include_examples": True,
            "fetch_current_knowledge": True
        }
    },
    {
        "name": "Non-Time-Sensitive (No Fetch)",
        "data": {
            "prompt": "explain recursion in programming",
            "context": "coding",
            "style": "detailed",
            "include_examples": True,
            "fetch_current_knowledge": False  # Disabled
        }
    }
]

print("=" * 70)
print("TESTING KNOWLEDGE INTEGRATION IN PROMPT ENHANCEMENT")
print("=" * 70)

for test in test_cases:
    print(f"\n{'='*70}")
    print(f"Test: {test['name']}")
    print(f"Knowledge Fetch: {'ENABLED' if test['data']['fetch_current_knowledge'] else 'DISABLED'}")
    print(f"{'='*70}")
    
    response = requests.post(url, json=test['data'])
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\nORIGINAL: {result['original_prompt']}")
        
        # Check for temporal context in enhanced prompt
        enhanced = result['enhanced_prompt']
        
        print(f"\nKNOWLEDGE INTEGRATION FEATURES:")
        features = []
        
        if "Current Date:" in enhanced:
            features.append("✓ Current date included")
        if "Knowledge Cutoff:" in enhanced:
            features.append("✓ Knowledge cutoff specified")
        if "Information Freshness:" in enhanced:
            features.append("✓ Freshness indicator")
        if "Current Information" in enhanced:
            features.append("✓ Real-time knowledge section")
        if "Note: Information current as of" in enhanced:
            features.append("✓ Temporal note added")
        if "recent developments" in enhanced.lower():
            features.append("✓ Recent developments mentioned")
            
        if features:
            for feature in features:
                print(f"  {feature}")
        else:
            print("  ℹ️  No specific knowledge integration features (may not be needed)")
            
        # Show first part of enhanced prompt
        print(f"\nENHANCED (first 600 chars):")
        print(enhanced[:600] + "..." if len(enhanced) > 600 else enhanced)
        
        print(f"\nSCORE: {result['score_before']['overall']} → {result['score_after']['overall']}")
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

print("\n" + "=" * 70)
print("KNOWLEDGE INTEGRATION BENEFITS:")
print("=" * 70)
print("""
1. TIME-SENSITIVE UPDATES: Automatically detects when current information is needed
2. TEMPORAL ANCHORING: Adds explicit dates to prevent confusion
3. CONTEXT FRESHNESS: Indicates when information was last updated
4. SMART DETECTION: Only fetches when actually needed (saves API calls)
5. CACHE-FRIENDLY: Can cache results for repeated queries
6. FALLBACK SAFE: Works even if knowledge fetch fails

This feature is especially valuable for:
- Technical documentation queries
- API/framework usage questions  
- Best practices inquiries
- Time-sensitive topics
- Rapidly evolving fields (AI, web dev, etc.)
""")