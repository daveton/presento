"""
模板API - 获取可用模板列表
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from core.template_config import list_templates

router = APIRouter()


class TemplateInfo(BaseModel):
    id: str
    name: str
    description: str


class TemplateListResponse(BaseModel):
    templates: List[TemplateInfo]


@router.get("/templates", response_model=TemplateListResponse)
async def get_templates():
    """
    获取所有可用模板列表
    """
    templates = list_templates()
    return TemplateListResponse(
        templates=[TemplateInfo(**t) for t in templates]
    )
