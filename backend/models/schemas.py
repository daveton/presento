from pydantic import BaseModel, Field
from typing import List, Optional

class GenerateRequest(BaseModel):
    input: str = Field(..., description="Video URL or transcript text", min_length=1, max_length=5000)

class Slide(BaseModel):
    type: str
    title: str
    subtitle: Optional[str] = None
    points: Optional[List[str]] = None

class GenerateResponse(BaseModel):
    title: str
    slides: List[Slide]
    download_url: Optional[str] = None
