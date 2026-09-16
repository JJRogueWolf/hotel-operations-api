from typing import Annotated, Literal
from pydantic import BaseModel, Field, StringConstraints

Description = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=3,
        max_length=500
    )
]

class IssueCreate(BaseModel):
    room: int = Field(gt=0)
    description: Description

class IssueResponse(BaseModel):
    id: int
    room: int
    description: str
    status: Literal["Open", "Closed"]
    
class IssueListResponse(BaseModel):
    issues: list[IssueResponse]