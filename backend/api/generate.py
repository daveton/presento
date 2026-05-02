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
    生成PPT主接口 V2
    流程：验证 → Pipeline V2 (intent → structure → llm → rewrite → adapter → render)
    """
    # Step 0: Input validation
    is_valid, message = is_valid_input(request.input)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    try:
        # Step 1: Pipeline V2 - 新的意图驱动流程
        from core.pipeline import run_pipeline

        result = run_pipeline(request.input, template="business")

        # 构建标准响应格式
        content = {
            "title": result["title"],
            "slides": result["slides"]
        }

        # Step 2: Create PPT file
        download_url = await create_ppt_file(content)

        return GenerateResponse(
            title=content["title"],
            slides=content["slides"],
            download_url=download_url
        )
    except Exception as e:
        print(f"[API Error] {e}")
        # Fallback to old pipeline on error
        try:
            content = await generate_ppt_content(request.input)
            download_url = await create_ppt_file(content)
            return GenerateResponse(
                title=content["title"],
                slides=content["slides"],
                download_url=download_url
            )
        except Exception as e2:
            raise HTTPException(status_code=500, detail=str(e2))


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
