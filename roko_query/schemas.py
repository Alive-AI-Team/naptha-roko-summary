from pydantic import BaseModel

class InputSchema(BaseModel):
    question: str
    input_dir: str
