from typing import Optional
from pydantic import BaseModel
from datetime import datetime
# DTO : Data Transfert Object


class Product_POST_Body (BaseModel):
    productName: str
    productPrice: float


class Product_PATCH_Body (BaseModel):
    newFeature: bool

class Customer_response (BaseModel):
    id: int
    email: str
    create_at: datetime
    class Config:
        orm_mode: True