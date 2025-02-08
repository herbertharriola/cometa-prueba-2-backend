from pydantic import BaseModel

class Beer(BaseModel):
    name: str
    price: float
    quantity: int