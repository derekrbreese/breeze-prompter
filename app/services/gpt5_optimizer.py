"""
GPT-5 Prompt Optimization Guidelines
====================================

This module contains specialized instructions and patterns for optimizing
prompts specifically for next-generation models like GPT-5.
"""

GPT5_OPTIMIZATION_PRINCIPLES = """
# GPT-5 Prompt Engineering Principles

## 1. REASONING TRANSPARENCY
- Always request step-by-step reasoning chains
- Ask for explicit thought processes before conclusions
- Include "show your work" instructions for complex tasks
- Request confidence levels and uncertainty acknowledgment

## 2. MULTI-MODAL AWARENESS
- Prepare prompts for potential image/audio/video inputs
- Include placeholder syntax for non-text content: [IMAGE: description]
- Specify output modality preferences when relevant
- Consider cross-modal reasoning capabilities

## 3. CONTEXT WINDOW OPTIMIZATION
- Structure prompts for potentially massive context windows (1M+ tokens)
- Use hierarchical organization with clear section markers
- Include explicit relevance indicators for different context sections
- Design for selective attention mechanisms

## 4. CAPABILITY ASSUMPTIONS
- Avoid over-explaining basic concepts (assume stronger baseline)
- Focus on nuanced constraints and edge cases
- Request meta-cognitive reflection on approach selection
- Enable self-correction and iterative refinement

## 5. SAFETY AND ALIGNMENT
- Include explicit ethical constraints where relevant
- Request consideration of potential misuse or harm
- Ask for alternative approaches when primary path is problematic
- Build in verification steps for critical outputs

## 6. STRUCTURED OUTPUT FORMATS
- Use explicit schema definitions (JSON, XML, YAML)
- Include validation rules within the prompt
- Request type annotations and data contracts
- Specify error handling expectations

## 7. CHAIN-OF-THOUGHT VARIATIONS
- Few-shot reasoning: Provide 2-3 exemplar reasoning chains
- Zero-shot CoT: "Let's think step by step about this"
- Tree-of-thought: "Consider multiple solution paths"
- Self-consistency: "Generate N solutions and select the best"

## 8. TASK DECOMPOSITION
- Break complex tasks into atomic subtasks
- Include dependency graphs for multi-step processes
- Specify checkpoints and validation criteria
- Enable parallel processing where possible

## 9. PROMPT INJECTION RESISTANCE
- Use clear delimiters for user input: <<<USER_INPUT>>>
- Include explicit instruction boundaries
- Add meta-instructions about instruction following
- Implement output validation rules

## 10. PERFORMANCE OPTIMIZATION
- Include computational hints: "This requires careful analysis"
- Specify acceptable latency/quality tradeoffs
- Request streaming for long outputs
- Enable early stopping criteria
"""

GPT5_PROMPT_TEMPLATE = """
<TASK_SPECIFICATION>
{task_description}
</TASK_SPECIFICATION>

<REASONING_REQUIREMENTS>
- Provide step-by-step reasoning before any conclusions
- Rate confidence (0-100%) for each major claim
- Identify key assumptions and potential edge cases
- Consider alternative approaches before committing
</REASONING_REQUIREMENTS>

<OUTPUT_SPECIFICATION>
Format: {output_format}
Schema: {output_schema}
Constraints: {constraints}
Validation: {validation_rules}
</OUTPUT_SPECIFICATION>

<CONTEXT_HIERARCHY>
Primary Context (critical for task):
{primary_context}

Secondary Context (helpful but not essential):
{secondary_context}

Background (for reference only):
{background_context}
</CONTEXT_HIERARCHY>

<SAFETY_GUIDELINES>
- Ensure outputs are factual and verifiable
- Flag any potentially harmful implications
- Suggest safer alternatives if concerns arise
- Include disclaimers where appropriate
</SAFETY_GUIDELINES>

<EXECUTION_INSTRUCTIONS>
1. Parse and validate the task specification
2. Plan your approach using tree-of-thought
3. Execute with step-by-step reasoning
4. Self-verify against requirements
5. Format output according to specification
6. Include confidence scores and limitations
</EXECUTION_INSTRUCTIONS>
"""

def enhance_for_gpt5(prompt: str, context: str) -> dict:
    """
    Enhance a prompt specifically for GPT-5 capabilities
    """
    enhancements = {
        "reasoning_chain": "Add explicit CoT instructions",
        "structure": "Use hierarchical XML-like tags",
        "validation": "Include output schema and validation rules",
        "safety": "Add alignment and safety constraints",
        "multimodal": "Prepare for potential multi-modal inputs",
        "meta_cognitive": "Request reflection on approach",
        "confidence": "Ask for uncertainty quantification"
    }
    return enhancements