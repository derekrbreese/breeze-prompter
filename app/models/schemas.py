from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class PromptContext(str, Enum):
    CODING = "coding"
    WRITING = "writing"
    ANALYSIS = "analysis"
    CREATIVE = "creative"
    TECHNICAL = "technical"
    GENERAL = "general"


class PromptStyle(str, Enum):
    CONCISE = "concise"
    DETAILED = "detailed"
    TECHNICAL = "technical"
    CONVERSATIONAL = "conversational"


class PromptRequest(BaseModel):
    prompt: str = Field(..., description="The original prompt to be enhanced")
    context: Optional[PromptContext] = Field(
        default=PromptContext.GENERAL,
        description="The domain or context for the prompt"
    )
    style: Optional[PromptStyle] = Field(
        default=PromptStyle.DETAILED,
        description="The preferred style for the enhanced prompt"
    )
    include_examples: Optional[bool] = Field(
        default=False,
        description="Whether to include examples in the enhanced prompt"
    )
    fetch_current_knowledge: Optional[bool] = Field(
        default=False,
        description="Whether to fetch current information from web search for time-sensitive topics"
    )


class Improvement(BaseModel):
    category: str = Field(..., description="The category of improvement")
    description: str = Field(..., description="Description of the improvement")
    before: Optional[str] = Field(None, description="The original text")
    after: Optional[str] = Field(None, description="The improved text")


class PromptScore(BaseModel):
    clarity: int = Field(..., ge=0, le=100, description="Clarity score (0-100)")
    specificity: int = Field(..., ge=0, le=100, description="Specificity score (0-100)")
    completeness: int = Field(..., ge=0, le=100, description="Completeness score (0-100)")
    overall: int = Field(..., ge=0, le=100, description="Overall effectiveness score (0-100)")


class PromptResponse(BaseModel):
    original_prompt: str = Field(..., description="The original input prompt")
    enhanced_prompt: str = Field(..., description="The optimized version of the prompt")
    improvements: List[Improvement] = Field(..., description="List of specific improvements made")
    explanation: str = Field(..., description="Explanation of why the enhanced version is more effective")
    score_before: PromptScore = Field(..., description="Score of the original prompt")
    score_after: PromptScore = Field(..., description="Score of the enhanced prompt")
    tips: Optional[List[str]] = Field(None, description="Additional tips for future prompts")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")