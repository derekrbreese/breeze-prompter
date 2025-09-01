from fastapi import APIRouter, HTTPException
from app.models import (
    PromptRequest, PromptResponse, ErrorResponse,
    GPTPromptRequest, GPTPromptResponse
)
from app.services import PromptEnhancer

router = APIRouter()
enhancer = PromptEnhancer()


@router.post(
    "/perfect-prompt",
    response_model=PromptResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Perfect a prompt",
    description="Analyzes and enhances a prompt to make it more effective for AI systems"
)
async def perfect_prompt(request: PromptRequest) -> PromptResponse:
    """
    Enhance a prompt to make it more effective for AI systems.
    
    This endpoint takes a user's prompt and:
    - Analyzes it for clarity, specificity, and completeness
    - Identifies ambiguities and missing information
    - Generates an enhanced version with improvements
    - Provides explanations and scores for both versions
    """
    try:
        if not request.prompt or len(request.prompt.strip()) < 5:
            raise HTTPException(
                status_code=400,
                detail="Prompt must be at least 5 characters long"
            )
        
        if len(request.prompt) > 5000:
            raise HTTPException(
                status_code=400,
                detail="Prompt must be less than 5000 characters"
            )
        
        response = await enhancer.enhance_prompt(request)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error enhancing prompt: {str(e)}"
        )


@router.post(
    "/gpt-enhance",
    response_model=GPTPromptResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Enhance prompt for GPT (simplified)",
    description="Simplified endpoint for GPT custom actions - returns only the enhanced prompt"
)
async def gpt_enhance_prompt(request: GPTPromptRequest) -> GPTPromptResponse:
    """
    Enhance a prompt for GPT custom actions.
    
    This endpoint is optimized for ChatGPT custom actions:
    - Accepts document context for additional information
    - Returns only the enhanced prompt (no metadata)
    - Supports fetching current information for time-sensitive queries
    """
    try:
        if not request.prompt or len(request.prompt.strip()) < 5:
            raise HTTPException(
                status_code=400,
                detail="Prompt must be at least 5 characters long"
            )
        
        # Handle document context intelligently
        if request.document_context:
            # For prompts with document context, create a focused enhancement
            enhanced_prompt = await enhancer.enhance_with_document(
                prompt=request.prompt,
                document=request.document_context,
                context=request.context,
                style=request.style
            )
            return GPTPromptResponse(enhanced_prompt=enhanced_prompt)
        
        # For regular prompts without documents
        full_request = PromptRequest(
            prompt=request.prompt,
            context=request.context,
            style=request.style,
            include_examples=False,
            fetch_current_knowledge=request.fetch_current_info
        )
        
        # Get the full response
        full_response = await enhancer.enhance_prompt(full_request)
        
        # Return only the enhanced prompt
        return GPTPromptResponse(enhanced_prompt=full_response.enhanced_prompt)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error enhancing prompt: {str(e)}"
        )


@router.get(
    "/health",
    summary="Health check",
    description="Check if the API is running"
)
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Breese Prompter API"}