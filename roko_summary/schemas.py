from pydantic import BaseModel
from typing import List


class InputSchema(BaseModel):
    start_date: str
    end_date: str
    sources: List[str]
