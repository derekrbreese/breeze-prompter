"""
Intelligent role detection for prompt enhancement
"""

from typing import Optional, Tuple
from app.models import PromptContext


class RoleDetector:
    """Determines when role establishment is beneficial"""
    
    # Keywords that suggest simple queries (no role needed)
    SIMPLE_QUERY_INDICATORS = {
        "what is", "what's", "how many", "how much", "when is", "when was",
        "where is", "where are", "list", "name", "define", "calculate",
        "convert", "translate", "what time", "what date", "who is", "who was"
    }
    
    # Keywords that benefit from role establishment
    ROLE_BENEFICIAL_INDICATORS = {
        "write", "create", "design", "analyze", "review", "optimize", "debug",
        "explain like", "act as", "pretend", "imagine", "develop", "architect",
        "diagnose", "troubleshoot", "evaluate", "assess", "critique", "refactor"
    }
    
    # Context-to-role mapping
    CONTEXT_ROLES = {
        PromptContext.CODING: "expert software engineer",
        PromptContext.WRITING: "professional writer and editor",
        PromptContext.ANALYSIS: "data analyst",
        PromptContext.CREATIVE: "creative professional",
        PromptContext.TECHNICAL: "technical expert",
        PromptContext.GENERAL: None  # Determined by content
    }
    
    @classmethod
    def needs_role(cls, prompt: str, context: PromptContext) -> Tuple[bool, Optional[str]]:
        """
        Determine if a prompt needs role establishment
        
        Returns:
            Tuple of (needs_role: bool, suggested_role: Optional[str])
        """
        prompt_lower = prompt.lower().strip()
        
        # Check for simple queries
        if any(prompt_lower.startswith(indicator) for indicator in cls.SIMPLE_QUERY_INDICATORS):
            return False, None
        
        # Check prompt length (very short prompts usually don't need roles)
        if len(prompt.split()) < 5:
            return False, None
        
        # Check if prompt already includes a role
        if any(phrase in prompt_lower for phrase in ["you are", "act as", "pretend to be", "imagine you're"]):
            return False, None  # Already has role establishment
        
        # Check for role-beneficial indicators
        needs_role = any(indicator in prompt_lower for indicator in cls.ROLE_BENEFICIAL_INDICATORS)
        
        # Context-specific checks
        if context in [PromptContext.CODING, PromptContext.WRITING, PromptContext.TECHNICAL]:
            needs_role = True  # These contexts usually benefit from roles
        
        if needs_role:
            # Determine the appropriate role
            role = cls.CONTEXT_ROLES.get(context)
            
            # Analyze prompt for specific role needs
            if not role or context == PromptContext.GENERAL:
                if any(word in prompt_lower for word in ["code", "program", "function", "algorithm"]):
                    role = "expert software engineer"
                elif any(word in prompt_lower for word in ["essay", "article", "blog", "story"]):
                    role = "professional writer"
                elif any(word in prompt_lower for word in ["data", "statistics", "metrics", "analysis"]):
                    role = "data analyst"
                elif any(word in prompt_lower for word in ["design", "ui", "ux", "interface"]):
                    role = "UI/UX designer"
                else:
                    role = "expert assistant"
            
            return True, role
        
        return False, None
    
    @classmethod
    def get_complexity_level(cls, prompt: str) -> str:
        """
        Determine the complexity level of a prompt using multiple factors
        
        Returns: "simple", "moderate", or "complex"
        """
        prompt_lower = prompt.lower()
        word_count = len(prompt.split())
        
        # Count complexity factors
        complexity_score = 0
        
        # 1. Check for simple query patterns (negative complexity)
        simple_patterns = [
            "what is", "what's", "how many", "how much", "when is", "when was",
            "where is", "list", "name", "define", "calculate", "convert", "translate"
        ]
        # Don't treat "explain" as simple
        explain_patterns = ["explain", "describe how", "how does", "how do"]
        if any(pattern in prompt_lower for pattern in simple_patterns):
            complexity_score -= 2
        elif any(pattern in prompt_lower for pattern in explain_patterns):
            complexity_score += 1  # Explanations need moderate detail
        
        # 2. Length-based scoring
        if word_count < 5:
            complexity_score -= 1
        elif word_count < 10:
            complexity_score += 0  # Neutral
        elif word_count < 20:
            complexity_score += 1
        elif word_count < 40:
            complexity_score += 2
        else:
            complexity_score += 3
        
        # 3. Multi-step or multi-requirement indicators
        multi_step_indicators = [
            "and then", "after that", "next", "finally", "first", "second",
            "step by step", "detailed", "comprehensive", "complete"
        ]
        multi_step_count = sum(1 for indicator in multi_step_indicators if indicator in prompt_lower)
        complexity_score += multi_step_count * 1.5
        
        # 4. Technical/specialized task indicators
        technical_indicators = [
            "implement", "architect", "design", "optimize", "refactor",
            "debug", "integrate", "deploy", "configure", "analyze",
            "evaluate", "compare", "benchmark", "profile", "test"
        ]
        technical_count = sum(1 for indicator in technical_indicators if indicator in prompt_lower)
        complexity_score += technical_count
        
        # 5. Creation/building indicators (usually complex)
        creation_indicators = [
            "build", "create", "develop", "make", "construct", "generate",
            "write a program", "write an app", "write a system", "build an app"
        ]
        # Check for creation with qualifiers
        for indicator in creation_indicators:
            if indicator in prompt_lower:
                # If it's just "create" or "make" with "simple", reduce complexity
                if "simple" in prompt_lower and indicator in ["create", "make"]:
                    complexity_score += 1
                else:
                    complexity_score += 3  # Increased weight for building tasks
        
        # 6. Scope indicators
        scope_indicators = {
            "simple": ["basic", "simple", "quick", "small"],
            "moderate": ["standard", "typical", "normal"],
            "complex": ["entire", "full", "complete", "comprehensive", "production", "enterprise", "scalable", "real-time", "production-ready"]
        }
        for scope, words in scope_indicators.items():
            if any(word in prompt_lower for word in words):
                if scope == "simple":
                    # Only reduce if not part of a creation task
                    if not any(create in prompt_lower for create in ["create", "build", "make"]):
                        complexity_score -= 1
                elif scope == "complex":
                    complexity_score += 3  # Increased weight
        
        # 7. Multiple entity handling
        multiple_indicators = [
            "multiple", "various", "different", "several", "many",
            "list of", "array of", "collection of"
        ]
        if any(indicator in prompt_lower for indicator in multiple_indicators):
            complexity_score += 1
        
        # 8. Constraint indicators
        constraint_indicators = [
            "must", "should", "need to", "require", "ensure",
            "make sure", "guarantee", "with", "without", "using"
        ]
        constraint_count = sum(1 for indicator in constraint_indicators if indicator in prompt_lower)
        if constraint_count > 2:
            complexity_score += 1
        
        # 9. Question complexity (single vs multi-part)
        question_marks = prompt.count('?')
        if question_marks > 1:
            complexity_score += question_marks - 1
        
        # 10. Check for code/technical content
        if any(char in prompt for char in ['()', '{}', '[]', '->', '=>', 'function', 'class', 'def']):
            complexity_score += 1
        
        # Determine final complexity level based on score
        if complexity_score <= -1:
            return "simple"
        elif complexity_score <= 3:
            return "moderate"
        else:
            return "complex"