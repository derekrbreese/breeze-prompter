#!/usr/bin/env python3
"""Test the improved complexity detection logic"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.role_detector import RoleDetector

test_prompts = [
    # Should be SIMPLE
    ("What's the capital of France?", "simple"),
    ("Calculate 15% of 200", "simple"),
    ("Convert 100 USD to EUR", "simple"),
    ("Define machine learning", "simple"),
    ("List 5 fruits", "simple"),
    
    # Should be MODERATE
    ("Write a Python function to reverse a string", "moderate"),
    ("Explain how photosynthesis works", "moderate"),
    ("Create a simple todo list in JavaScript", "moderate"),
    ("Compare Python and JavaScript", "moderate"),
    
    # Should be COMPLEX
    ("Build a real-time chat application with user authentication", "complex"),
    ("Create a comprehensive testing strategy for our e-commerce platform", "complex"),
    ("Design and implement a scalable microservices architecture", "complex"),
    ("Develop a machine learning model to predict customer churn with data preprocessing, feature engineering, model training, and evaluation", "complex"),
    ("Step by step guide to deploy a production-ready application", "complex"),
    
    # Edge cases
    ("build an app", "complex"),  # Short but complex task
    ("What is 2+2?", "simple"),   # Very simple
    ("Analyze customer data", "moderate"),  # Has "analyze" but short
]

print("Testing Complexity Detection")
print("=" * 60)

correct = 0
total = len(test_prompts)

for prompt, expected in test_prompts:
    detected = RoleDetector.get_complexity_level(prompt)
    needs_role, suggested_role = RoleDetector.needs_role(prompt, "general")
    
    is_correct = detected == expected
    if is_correct:
        correct += 1
        symbol = "✅"
    else:
        symbol = "❌"
    
    print(f"\n{symbol} Prompt: {prompt[:50]}...")
    print(f"   Expected: {expected}, Got: {detected}")
    if needs_role:
        print(f"   Role: {suggested_role}")

print(f"\n{'='*60}")
print(f"Accuracy: {correct}/{total} ({100*correct/total:.1f}%)")
print("=" * 60)