from fastapi import APIRouter, HTTPException
from models.schemas import GenerateRequest, GenerateResponse, Slide
from services.llm_service import generate_ppt_content, is_valid_input
from services.ppt_engine import create_ppt_file
import os

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
async def generate_ppt(request: GenerateRequest):
    # Step 0: Input validation
    is_valid, message = is_valid_input(request.input)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    try:
        # Step 1: Generate content with LLM (includes rewrite + quality scoring)
        content = await generate_ppt_content(request.input)
        
        # Step 2: Create PPT file
        download_url = await create_ppt_file(content)
        
        return GenerateResponse(
            title=content["title"],
            slides=content["slides"],
            download_url=download_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
