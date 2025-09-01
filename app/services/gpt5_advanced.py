"""
GPT-5 Advanced Prompt Engineering (2025)
========================================
Based on latest OpenAI GPT-5 documentation and best practices
"""

GPT5_SYSTEM_PROMPT = """You are an expert prompt engineer specializing in GPT-5 optimization (2025 techniques).

KEY GPT-5 CHARACTERISTICS:
- Substantial leap in agentic task performance
- Enhanced coding capabilities and raw intelligence
- Improved steerability and control spectrum
- Safety-trained with "safe completions" approach
- Optimized for structured prompt scaffolding

PROMPT ENHANCEMENT PRINCIPLES:

1. STRUCTURED PROMPT SCAFFOLDING
- Wrap inputs in defensive, guarded templates
- Use clear section markers: ### Instruction, ### Context, ### Evaluation
- Include redundant constraints for safety
- Implement prompt injection resistance

2. AGENTIC BEHAVIOR CALIBRATION
- Balance proactivity vs explicit guidance
- Control reasoning_effort parameter
- Limit tangential tool-calling when needed
- Specify scope boundaries clearly

3. TEMPORAL ANCHORING
- Include knowledge cutoff date
- Specify current date context
- Prevent temporal confusion
- Handle time-sensitive queries properly

4. CODE ENGINEERING RULES
- Organize engineering principles clearly
- Include directory structure context
- Reference existing dependencies
- Specify best practices upfront

5. CONTEXT HIERARCHY
- Primary context (critical)
- Secondary context (helpful)
- Background (reference only)
- Use explicit relevance indicators

6. SAFETY BOUNDARIES
- Implement safe completion patterns
- Allow partial answers when appropriate
- Include ethical constraints
- Add misuse prevention layers

7. EVALUATION CRITERIA
- Specify success metrics before task
- Include self-verification steps
- Add confidence scoring
- Request uncertainty acknowledgment

8. MODEL-SPECIFIC FORMATTING
- Use ### headers for GPT-5
- Implement rule hierarchies
- Add explicit evaluation criteria
- Structure for measurable improvements

9. FEW-SHOT OPTIMIZATION
- Include relevant examples in context
- Use User/Assistant message pairs
- Demonstrate edge cases
- Show expected output format

10. CONTRADICTION ELIMINATION
- Remove ambiguous instructions
- Avoid conflicting requirements
- Reduce latency through clarity
- Test for logical consistency
"""

GPT5_ENHANCED_TEMPLATE = """
### TASK SPECIFICATION
{task_description}

### TEMPORAL CONTEXT
Knowledge Cutoff: January 2025
Current Date: {current_date}
Time-Sensitive: {is_time_sensitive}

### ENGINEERING RULES
{engineering_principles}
Directory Structure: {directory_structure}
Dependencies: {dependencies}
Best Practices: {best_practices}

### CONTEXT HIERARCHY

#### Primary Context (Critical)
{primary_context}

#### Secondary Context (Helpful)
{secondary_context}

#### Background (Reference)
{background_context}

### AGENTIC BEHAVIOR CALIBRATION
Reasoning Effort: {reasoning_effort}
Proactivity Level: {proactivity_level}
Tool Usage Scope: {tool_scope}
Decision Authority: {decision_authority}

### INSTRUCTION
<<<USER_INPUT>>>
{user_input}
<<<END_USER_INPUT>>>

Think step-by-step through this task:
1. Parse and validate the input
2. Identify key requirements and constraints
3. Plan your approach with reasoning
4. Execute with explicit thought process
5. Self-verify against success criteria
6. Format output according to specification

### EVALUATION CRITERIA
Success Metrics:
{success_metrics}

Output Requirements:
{output_requirements}

Confidence Scoring:
- Provide confidence (0-100%) for each claim
- Acknowledge areas of uncertainty
- Flag assumptions made

### SAFETY BOUNDARIES
- Ensure factual accuracy
- Flag potential risks
- Suggest safer alternatives if needed
- Include appropriate disclaimers
- Follow safe completion patterns

### OUTPUT SPECIFICATION
Format: {output_format}
Schema: {output_schema}
Validation Rules: {validation_rules}
Error Handling: {error_handling}

### FEW-SHOT EXAMPLES
{examples}

### RESPONSE
Please provide your response following all specifications above.
Include your reasoning process and confidence scores.
"""

def optimize_for_gpt5(prompt: str, context: dict) -> dict:
    """
    Apply GPT-5 specific optimizations to a prompt
    
    Args:
        prompt: Original prompt text
        context: Dictionary containing context information
        
    Returns:
        Dictionary with optimization recommendations
    """
    optimizations = {
        "scaffolding": {
            "add_section_markers": True,
            "wrap_user_input": "<<<USER_INPUT>>>...<<<END_USER_INPUT>>>",
            "defensive_structure": True
        },
        "agentic_calibration": {
            "reasoning_effort": "high",  # Options: low, medium, high
            "proactivity": "balanced",   # Options: passive, balanced, proactive
            "tool_scope": "focused"      # Options: limited, focused, broad
        },
        "temporal": {
            "include_cutoff": "January 2025",
            "include_current_date": True,
            "time_sensitive_flag": False
        },
        "safety": {
            "safe_completions": True,
            "partial_answers_allowed": True,
            "ethical_constraints": True,
            "injection_resistance": True
        },
        "formatting": {
            "use_headers": "### Style Headers",
            "hierarchy_levels": 3,
            "evaluation_first": True
        },
        "context_engineering": {
            "primary_secondary_split": True,
            "relevance_indicators": True,
            "reference_existing_code": True
        },
        "validation": {
            "success_metrics": True,
            "confidence_scores": True,
            "self_verification": True,
            "uncertainty_acknowledgment": True
        },
        "optimization_tools": {
            "use_prompt_optimizer": True,
            "measure_improvements": True,
            "eliminate_contradictions": True
        }
    }
    
    return optimizations

# Specific patterns for different task types
TASK_SPECIFIC_PATTERNS = {
    "coding": {
        "include_dependencies": True,
        "reference_package_json": True,
        "directory_structure": True,
        "engineering_principles": True
    },
    "analysis": {
        "structured_evaluation": True,
        "confidence_intervals": True,
        "uncertainty_quantification": True,
        "multi_perspective": True
    },
    "creative": {
        "safety_boundaries": "relaxed",
        "proactivity": "high",
        "exploration_allowed": True
    },
    "factual": {
        "citation_required": True,
        "confidence_threshold": 80,
        "uncertainty_explicit": True,
        "temporal_accuracy": "critical"
    }
}