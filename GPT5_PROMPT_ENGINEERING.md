# GPT-5 Prompt Engineering Guide (2025)

## Key Nuances for GPT-5 Prompt Development

Based on the latest research and OpenAI documentation, here are the critical nuances built into this prompt enhancer for GPT-5:

### 1. **Structured Prompt Scaffolding (Defensive Prompting)**
- **What it is**: Wrapping user inputs in structured, guarded templates that limit misbehavior
- **Implementation**: 
  - Use `### Section Markers` for clear boundaries
  - Wrap user inputs: `<<<USER_INPUT>>>content<<<END_USER_INPUT>>>`
  - Add redundant constraints for safety
  - Include prompt injection resistance layers

### 2. **Agentic Behavior Calibration**
- **What it is**: GPT-5 can operate anywhere along the control spectrum
- **Key Parameters**:
  - `reasoning_effort`: low/medium/high (controls thoroughness vs speed)
  - `proactivity_level`: passive/balanced/proactive
  - `tool_scope`: limited/focused/broad
  - `decision_authority`: what the model can decide autonomously
- **Why it matters**: Prevents excessive tool-calling and reduces latency

### 3. **Temporal Anchoring**
- **What it is**: Explicitly stating knowledge cutoff and current date
- **Format**:
  ```
  Knowledge Cutoff: January 2025
  Current Date: [actual date]
  Time-Sensitive: Yes/No
  ```
- **Why it matters**: Prevents temporal confusion and hallucination of current events

### 4. **Context Hierarchy**
- **Structure**:
  - **Primary Context** (critical for task completion)
  - **Secondary Context** (helpful but not essential)
  - **Background** (reference only)
- **Why it matters**: GPT-5's attention mechanisms can better prioritize information

### 5. **Evaluation-First Design**
- **What it is**: Placing success criteria BEFORE the actual task
- **Benefits**:
  - Model knows what success looks like before starting
  - Enables self-verification
  - Reduces need for follow-up corrections
- **Format**:
  ```
  ### Evaluation Criteria
  [Success metrics here]
  
  ### Instruction
  [Task here]
  ```

### 6. **Safe Completions Pattern**
- **What it is**: GPT-5's new safety training approach
- **Implementation**:
  - Allow partial answers when full answer would be unsafe
  - Include ethical boundaries explicitly
  - Add misuse prevention layers
  - Flag potential risks proactively
- **Example**: "I can help with X aspect, but Y would require [safety consideration]"

### 7. **Contradiction Elimination**
- **Why it matters**: Contradictions reduce performance and increase latency
- **How to check**:
  - Ensure logical consistency across all instructions
  - Remove ambiguous requirements
  - Test for conflicting constraints
- **Impact**: Significantly improves reasoning model performance

### 8. **Few-Shot Optimization**
- **GPT-5 Specific**:
  - Include 2-3 high-quality examples
  - Show edge cases explicitly
  - Use User/Assistant message pairs for chat format
  - Demonstrate expected confidence scoring
- **Format**:
  ```
  ### Examples
  User: [input]
  Assistant: [output with confidence: 95%]
  ```

### 9. **Code Engineering Rules**
- **For coding tasks specifically**:
  - Include package.json/requirements.txt context
  - Specify directory structure
  - List engineering principles upfront
  - Reference existing dependencies
- **Why**: GPT-5 automatically searches for reference context but benefits from explicit structure

### 10. **Confidence and Uncertainty**
- **Requirements**:
  - Request confidence scores (0-100%) for all claims
  - Require explicit uncertainty acknowledgment
  - Ask for assumptions to be stated
  - Include self-verification steps
- **Format**: "Confidence: 85% - Assumption: [stated assumption]"

## API Usage Example

```python
import requests

# Your enhanced prompt API
url = "http://your-api/api/perfect-prompt"

# Original vague prompt
data = {
    "prompt": "build an app",
    "context": "coding",
    "style": "detailed",
    "include_examples": True
}

# Returns GPT-5 optimized prompt with:
# - Structured scaffolding
# - Temporal anchoring
# - Context hierarchy
# - Evaluation-first design
# - Safety boundaries
# - Confidence requirements
response = requests.post(url, json=data)
enhanced = response.json()["enhanced_prompt"]
```

## Key Differences from GPT-4

1. **More Structure**: GPT-5 benefits from redundant constraints and explicit sections
2. **Agentic Control**: Must calibrate proactivity level explicitly
3. **Safety Integration**: Safe completions allow partial answers
4. **Temporal Awareness**: Requires explicit anchoring to prevent confusion
5. **Evaluation Focus**: Success criteria before task improves outcomes
6. **Confidence Scoring**: Built-in uncertainty quantification expected

## Testing Your Prompts

The API automatically:
- Scores prompts before/after enhancement
- Validates for contradictions
- Checks for injection vulnerabilities
- Ensures temporal consistency
- Verifies safety boundaries
- Optimizes for GPT-5's specific capabilities

## Deployment for GPT Custom Actions

1. API provides OpenAPI schema at `/openapi.json`
2. Includes proper CORS headers for ChatGPT
3. Supports authentication via API keys
4. Returns structured JSON optimized for GPT consumption

## Continuous Improvement

As GPT-5 evolves, monitor:
- OpenAI's Prompt Optimizer tool recommendations
- New safety training patterns
- Updated best practices from OpenAI Cookbook
- Performance metrics on your specific use cases

This prompt enhancer implements all current (2025) best practices for GPT-5, ensuring your prompts leverage the model's enhanced agentic capabilities, improved reasoning, and safety features effectively.