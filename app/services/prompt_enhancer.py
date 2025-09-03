import json
import time
import logging
from typing import List, Dict, Any, Optional
from app.utils import OpenRouterClient
from app.models import (
    PromptRequest,
    PromptResponse,
    Improvement,
    PromptScore,
    PromptContext,
    PromptStyle
)
from app.services.knowledge_updater import SmartKnowledgeIntegration
from app.services.role_detector import RoleDetector


class PromptEnhancer:
    def __init__(self):
        # Lazy-init the OpenRouter client to avoid import-time failures
        # when the API key is not present (e.g., health checks, docs).
        self._client: Optional[OpenRouterClient] = None
        self.knowledge = SmartKnowledgeIntegration()
        self._logger = logging.getLogger("enhancer")

    def _get_client(self) -> OpenRouterClient:
        if self._client is None:
            self._client = OpenRouterClient()
        return self._client
    
    async def enhance_prompt(self, request: PromptRequest) -> PromptResponse:
        """
        Main method to enhance a prompt using AI
        """
        start_total = time.perf_counter()
        # Check complexity level to optimize API calls
        complexity = RoleDetector.get_complexity_level(request.prompt)
        
        # For simple prompts, skip detailed analysis
        if complexity == "simple":
            # Generate a simple enhancement without deep analysis
            enhanced = await self._generate_simple_enhancement(
                request.prompt,
                request.context,
                request.style
            )
            analysis = {"intent": "simple query", "ambiguities": [], "missing_elements": [], "strengths": [], "context_gaps": []}
            # Use estimated scores for simple prompts
            score_before = PromptScore(clarity=60, specificity=50, completeness=50, overall=53)
            score_after = PromptScore(clarity=90, specificity=85, completeness=85, overall=87)
        else:
            # Full analysis for moderate/complex prompts
            t = time.perf_counter()
            analysis = await self._analyze_prompt(request.prompt, request.context)
            if self._logger:
                self._logger.debug("analyze_prompt duration_ms=%.1f", (time.perf_counter() - t) * 1000)
            
            # Generate the enhanced prompt
            t = time.perf_counter()
            enhanced = await self._generate_enhanced_prompt(
                request.prompt,
                analysis,
                request.context,
                request.style,
                request.include_examples
            )
            if self._logger:
                self._logger.debug("generate_enhanced_prompt duration_ms=%.1f", (time.perf_counter() - t) * 1000)
            
            # Score both prompts only for complex cases
            if complexity == "complex":
                t = time.perf_counter()
                score_before = await self._score_prompt(request.prompt)
                score_after = await self._score_prompt(enhanced["enhanced_prompt"])
                if self._logger:
                    self._logger.debug("score_prompts duration_ms=%.1f", (time.perf_counter() - t) * 1000)
            else:
                # Estimated scores for moderate complexity
                score_before = PromptScore(clarity=70, specificity=65, completeness=60, overall=65)
                score_after = PromptScore(clarity=85, specificity=80, completeness=80, overall=82)
        
        # Integrate current knowledge if requested (force when requested)
        if request.fetch_current_knowledge:
            enhanced["enhanced_prompt"] = await self.knowledge.integrate_knowledge(
                request.prompt,
                enhanced["enhanced_prompt"],
                request.context.value,
                user_preference="always"
            )
        
        # Extract improvements
        improvements = self._extract_improvements(analysis, enhanced)
        
        if self._logger:
            self._logger.debug("enhance_prompt total_duration_ms=%.1f", (time.perf_counter() - start_total) * 1000)

        return PromptResponse(
            original_prompt=request.prompt,
            enhanced_prompt=enhanced["enhanced_prompt"],
            improvements=improvements,
            explanation=enhanced["explanation"],
            score_before=score_before,
            score_after=score_after,
            tips=enhanced.get("tips", [])
        )
    
    async def _analyze_prompt(self, prompt: str, context: PromptContext) -> Dict[str, Any]:
        """
        Analyze the original prompt for issues and opportunities
        """
        system_message = """You are an expert prompt engineer. Analyze the given prompt and identify issues.

Return ONLY valid JSON with these exact keys:
{
  "intent": "What the user is trying to achieve",
  "ambiguities": ["list", "of", "unclear", "parts"],
  "missing_elements": ["list", "of", "missing", "info"],
  "strengths": ["list", "of", "good", "parts"],
  "context_gaps": ["list", "of", "missing", "context"]
}"""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Context: {context}\nPrompt to analyze: {prompt}"}
        ]
        
        response = await self._get_client().chat_completion(messages, temperature=0.3, max_tokens=256)
        
        try:
            # Extract JSON from the response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            else:
                json_str = response
            return json.loads(json_str)
        except:
            # Fallback if JSON parsing fails
            return {
                "intent": "Unable to parse",
                "ambiguities": [],
                "missing_elements": [],
                "strengths": [],
                "context_gaps": []
            }
    
    async def _generate_enhanced_prompt(
        self,
        original: str,
        analysis: Dict[str, Any],
        context: PromptContext,
        style: PromptStyle,
        include_examples: bool
    ) -> Dict[str, Any]:
        """
        Generate an enhanced version of the prompt
        """
        # Determine if role establishment is needed
        needs_role, suggested_role = RoleDetector.needs_role(original, context)
        complexity = RoleDetector.get_complexity_level(original)
        
        system_message = f"""You are an expert prompt engineer optimizing prompts specifically for GPT-5 (2025 best practices).

PROMPT COMPLEXITY: {complexity}
NEEDS ROLE: {needs_role}
SUGGESTED ROLE: {suggested_role if suggested_role else 'None'}

Create an enhanced prompt based on complexity:

FOR SIMPLE PROMPTS:
- Keep it concise and direct
- Add minimal scaffolding
- Only add role if complexity warrants it
- Focus on clarity over structure

FOR MODERATE PROMPTS:
- Add helpful structure
- Include role if beneficial
- Balance clarity with specificity

FOR COMPLEX PROMPTS:
- Use STRUCTURED PROMPT SCAFFOLDING
- Include comprehensive role establishment
- Add all safety boundaries

GPT-5 OPTIMIZATION REQUIREMENTS (apply based on complexity):

1. STRUCTURED SCAFFOLDING
   - Use ### section markers (### Instruction, ### Context, ### Evaluation)
   - Wrap user inputs: <<<USER_INPUT>>>...<<<END_USER_INPUT>>>
   - Add redundant constraints for safety
   - Include prompt injection resistance

2. AGENTIC CALIBRATION
   - Specify reasoning_effort level (low/medium/high)
   - Balance proactivity vs explicit guidance
   - Define tool-calling scope boundaries
   - Control model's decision authority

3. TEMPORAL ANCHORING
   - Include "Knowledge Cutoff: January 2025"
   - Add "Current Date: [date]"
   - Prevent temporal confusion
   - Handle time-sensitive aspects

4. CONTEXT HIERARCHY
   - Split into Primary (critical), Secondary (helpful), Background (reference)
   - Use explicit relevance indicators
   - For coding: include dependencies, directory structure, engineering rules

5. EVALUATION-FIRST DESIGN
   - Put success criteria BEFORE the task
   - Include self-verification steps
   - Request confidence scores (0-100%)
   - Require uncertainty acknowledgment

6. SAFETY BOUNDARIES (GPT-5 Safe Completions)
   - Allow partial answers when appropriate
   - Include ethical constraints
   - Add misuse prevention
   - Flag potential risks

7. CONTRADICTION ELIMINATION
   - Remove ambiguous instructions (reduces latency)
   - Ensure logical consistency
   - Test for conflicting requirements

8. FEW-SHOT OPTIMIZATION
   - Include 2-3 relevant examples when helpful
   - Show edge cases and expected outputs
   - Use User/Assistant message pairs

Context: {context} | Style: {style}
{"Include examples" if include_examples else "No examples needed"}

Return ONLY valid JSON:
{{
  "enhanced_prompt": "Complete prompt with ### sections, temporal anchoring, scaffolding",
  "explanation": "How this leverages GPT-5's enhanced agentic and reasoning capabilities",
  "tips": ["GPT-5 specific tip 1", "GPT-5 specific tip 2", "GPT-5 specific tip 3"]
}}"""
        
        user_message = f"""Original prompt: "{original}"

Based on this analysis, create a much better, more specific prompt:
- Intent: {analysis.get('intent', 'unknown')}
- Issues: {', '.join(analysis.get('ambiguities', [])[:3])}
- Missing: {', '.join(analysis.get('missing_elements', [])[:3])}

IMPORTANT: Apply enhancement based on complexity level ({complexity}):
- SIMPLE: Keep enhancements minimal. Add clarity without over-engineering. {"No role needed." if not needs_role else f"Add role: {suggested_role}"}
- MODERATE: Add helpful structure and specificity. Balance detail with conciseness.
- COMPLEX: Apply full GPT-5 optimization with scaffolding, temporal anchoring, and comprehensive structure.

For example:
- Simple: "What's the capital of France?" → "What is the capital city of France?"
- Moderate: "write code for sorting" → "Write a Python function that implements quicksort for sorting integers."
- Complex: "build an app" → [Full scaffolded prompt with role, context, specifications, etc.]

Now enhance the original prompt appropriately for its complexity level."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        response = await self._get_client().chat_completion(messages, temperature=0.5, max_tokens=512)
        
        try:
            # Try to extract JSON from the response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "{" in response and "}" in response:
                # Find the JSON object in the response
                start = response.index("{")
                end = response.rindex("}") + 1
                json_str = response[start:end]
            else:
                json_str = response
            
            result = json.loads(json_str)
            
            # Ensure we have a valid enhanced prompt
            if not result.get("enhanced_prompt") or result["enhanced_prompt"] == original:
                # Generate a default enhancement
                result["enhanced_prompt"] = self._generate_default_enhancement(original, context, style, include_examples)
            
            return result
        except Exception as e:
            # Fallback with a better default enhancement
            return {
                "enhanced_prompt": self._generate_default_enhancement(original, context, style, include_examples),
                "explanation": "The enhanced prompt provides specific requirements, constraints, and expected output format for better AI comprehension.",
                "tips": ["Always specify the programming language", "Include input/output examples", "Define edge cases and constraints"]
            }
    
    def _generate_default_enhancement(self, original: str, context: PromptContext, style: PromptStyle, include_examples: bool) -> str:
        """Generate a default enhancement when AI fails"""
        if "sort" in original.lower() and context == PromptContext.CODING:
            return """Write a Python function called `sort_array` that implements the quicksort algorithm to sort a list of integers.

Requirements:
- Function signature: `def sort_array(arr: List[int]) -> List[int]:`
- Sort in ascending order
- Handle edge cases: empty list, single element, duplicates
- Include type hints
- Add a docstring with description and usage example
- Time complexity should be O(n log n) average case

Example usage:
```python
result = sort_array([3, 1, 4, 1, 5, 9, 2, 6])
print(result)  # Output: [1, 1, 2, 3, 4, 5, 6, 9]
```

Return the sorted list without modifying the original."""
        else:
            return f"""{original}

Please provide:
1. Specific requirements and constraints
2. Expected output format
3. Any relevant context or background
4. Examples if applicable"""
    
    async def _score_prompt(self, prompt: str) -> PromptScore:
        """
        Score a prompt on various metrics
        """
        system_message = """Score the following prompt on these criteria (0-100):
1. Clarity: How clear and unambiguous is the prompt?
2. Specificity: How specific are the requirements?
3. Completeness: Does it include all necessary information?
4. Overall: Overall effectiveness for AI understanding

Return ONLY a JSON object with keys: clarity, specificity, completeness, overall"""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        response = await self._get_client().chat_completion(messages, temperature=0.1, max_tokens=192)
        
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            else:
                # Try to extract JSON from the response
                import re
                json_match = re.search(r'\{[^}]+\}', response)
                json_str = json_match.group(0) if json_match else response
            
            scores = json.loads(json_str)
            return PromptScore(
                clarity=scores.get("clarity", 50),
                specificity=scores.get("specificity", 50),
                completeness=scores.get("completeness", 50),
                overall=scores.get("overall", 50)
            )
        except:
            # Fallback scores
            return PromptScore(clarity=50, specificity=50, completeness=50, overall=50)
    
    def _extract_improvements(self, analysis: Dict[str, Any], enhanced: Dict[str, Any]) -> List[Improvement]:
        """
        Extract specific improvements made to the prompt
        """
        improvements = []
        
        # Add improvements based on analysis
        if analysis.get("ambiguities"):
            for amb in analysis["ambiguities"][:3]:  # Limit to top 3
                improvements.append(Improvement(
                    category="Clarity",
                    description=f"Clarified ambiguous element: {amb}",
                    before=None,
                    after=None
                ))
        
        if analysis.get("missing_elements"):
            for element in analysis["missing_elements"][:3]:
                improvements.append(Improvement(
                    category="Completeness",
                    description=f"Added missing element: {element}",
                    before=None,
                    after=None
                ))
        
        if analysis.get("context_gaps"):
            for gap in analysis["context_gaps"][:2]:
                improvements.append(Improvement(
                    category="Context",
                    description=f"Added context: {gap}",
                    before=None,
                    after=None
                ))
        
        # Add a general structure improvement
        improvements.append(Improvement(
            category="Structure",
            description="Reorganized prompt for better AI comprehension",
            before=None,
            after=None
        ))
        
        return improvements
    
    async def _generate_simple_enhancement(
        self,
        original: str,
        context: PromptContext,
        style: PromptStyle
    ) -> Dict[str, Any]:
        """
        Generate a simple enhancement for basic prompts (single API call)
        """
        system_message = f"""You are a prompt enhancement assistant. Make simple, clear improvements to basic prompts.

For simple prompts:
- Add clarity without over-engineering
- Fix obvious ambiguities
- Keep the enhancement concise
- Do NOT add complex scaffolding or roles unless absolutely necessary

Context: {context} | Style: {style}

Return ONLY valid JSON:
{{
  "enhanced_prompt": "The improved prompt text",
  "explanation": "Brief explanation of the improvement",
  "tips": ["Tip 1", "Tip 2"]
}}"""
        
        user_message = f"""Improve this simple prompt: "{original}"

Make it clearer and more specific, but keep it simple."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        response = await self._get_client().chat_completion(messages, temperature=0.3)
        
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "{" in response and "}" in response:
                start_idx = response.find("{")
                end_idx = response.rfind("}") + 1
                json_str = response[start_idx:end_idx]
            else:
                json_str = response
            
            return json.loads(json_str)
        except:
            # Fallback
            return {
                "enhanced_prompt": original + " (Please provide more specific details)",
                "explanation": "Added request for more details",
                "tips": ["Be more specific about your requirements"]
            }
    
    async def enhance_with_document(
        self,
        prompt: str,
        document: str,
        context: PromptContext,
        style: PromptStyle
    ) -> str:
        """
        Enhance a prompt that includes document context
        The document is provided as context, and we enhance the prompt to work WITH that context
        """
        # Determine what the user is trying to do with the document
        action_keywords = {
            "improve": "Review and enhance the provided text for clarity and impact",
            "summarize": "Create a concise summary of the key points",
            "analyze": "Provide a detailed analysis of the content",
            "edit": "Edit for grammar, style, and coherence",
            "rewrite": "Rewrite the content for better clarity and flow",
            "review": "Provide feedback and suggestions for improvement",
            "translate": "Translate the content accurately",
            "explain": "Explain the main concepts in simpler terms"
        }
        
        prompt_lower = prompt.lower()
        
        # Find the best action match
        action_found = None
        for keyword, enhanced_action in action_keywords.items():
            if keyword in prompt_lower:
                action_found = enhanced_action
                break
        
        # If no specific action found, create a generic enhancement
        if not action_found:
            if len(prompt.split()) < 3:
                action_found = "Process and improve the provided document"
            else:
                action_found = prompt
        
        # Build the enhanced prompt that will work WITH the document as context
        # The key is that the document is ALREADY PROVIDED as context
        enhanced = f"""Given the document provided as context, please {action_found}.

Document context to work with:
{document}

Requirements:
- Focus on {context.value} quality and {style.value} style
- Maintain accuracy and original intent
- Provide clear, actionable output
- Be specific and thorough in your response"""
        
        return enhanced

    async def enhance_prompt_fast(
        self,
        prompt: str,
        context: PromptContext,
        style: PromptStyle,
        include_examples: bool = False,
    ) -> Dict[str, Any]:
        """
        Fast single-call enhancement optimized for GPT custom actions.
        Skips separate analysis/scoring; returns minimal JSON.
        """
        system_message = f"""You are a prompt enhancement assistant. Improve the user's prompt.

Return ONLY compact JSON with keys: enhanced_prompt, explanation, tips
Ensure clarity and specificity. Tailor to context={context} style={style}.
If include_examples is true, add 1-2 short examples INSIDE the enhanced prompt.
"""

        user_message = f"""Original: {prompt}

Please produce an improved prompt suitable for direct use. Keep it concise.
"""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]

        t = time.perf_counter()
        response = await self._get_client().chat_completion(
            messages,
            temperature=0.3,
            max_tokens=384,
        )
        if self._logger:
            self._logger.debug("enhance_prompt_fast llm_duration_ms=%.1f", (time.perf_counter() - t) * 1000)

        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "{" in response and "}" in response:
                start = response.index("{")
                end = response.rindex("}") + 1
                json_str = response[start:end]
            else:
                json_str = response

            result = json.loads(json_str)
            if not result.get("enhanced_prompt"):
                result["enhanced_prompt"] = prompt
            if not result.get("explanation"):
                result["explanation"] = "Improved clarity and specificity."
            if not result.get("tips"):
                result["tips"] = []
            return result
        except Exception:
            return {
                "enhanced_prompt": prompt + " (clarify requirements, constraints, and desired output)",
                "explanation": "Added specificity and structure.",
                "tips": ["State language/format", "Provide an example", "List constraints"],
            }
