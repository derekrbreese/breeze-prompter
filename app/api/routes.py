from fastapi import APIRouter, HTTPException
from app.models import PromptRequest, PromptResponse, ErrorResponse
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


@router.get(
    "/health",
    summary="Health check",
    description="Check if the API is running"
)
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Breese Prompter API"}