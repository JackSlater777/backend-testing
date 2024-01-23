from pydantic import BaseModel
from datetime import datetime
from framework.enums.services.trading_app.degree import DegreeType
from typing import Optional


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[list[Degree]] = []
