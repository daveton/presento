from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from models.schemas import GenerateRequest, GenerateResponse
from infra.llm.client import generate_ppt_content, is_valid_input
from core.renderer import create_ppt_file
import os

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
async def generate_ppt(request: GenerateRequest):
    """
    生成PPT主接口
    流程：验证 → LLM生成 → 规则引擎 → 渲染 → 返回下载链接
    """
    # Step 0: Input validation
    is_valid, message = is_valid_input(request.input)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    try:
        # Step 1: Generate content with LLM (includes rewrite + quality scoring)
        content = await generate_ppt_content(request.input)
        
        # Step 2: Create PPT file (includes rules enforcement)
        download_url = await create_ppt_file(content)
        
        return GenerateResponse(
            title=content["title"],
            slides=content["slides"],
            download_url=download_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_ppt(filename: str):
    """
    下载PPT文件
    """
    # 安全检查：防止路径遍历
    if ".." in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    filepath = f"/tmp/presento/{filename}"
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        filepath,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=filename
    )
