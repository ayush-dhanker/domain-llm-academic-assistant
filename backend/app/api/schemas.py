from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)
    top_k: Optional[int] = Field(default=None, ge=1, le=10)


class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
