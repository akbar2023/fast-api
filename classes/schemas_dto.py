from datetime import datetime
from datetime import date
from pydantic import BaseModel
from typing import Optional

# DTO 

class Smartphone_POST_Body (BaseModel):
    brand: str
    model: str
    ram: int
    camera_front: int
    camera_back: int
    color: str
    price: float
    release_date: date
    is_available: Optional[bool]

class Smartphone_PATCH_Body (BaseModel):
    is_available: bool

class Smartphone_GETID_Response(BaseModel): # format de sortie (response)
    id: int
    brand: str
    model: str
    ram: int
    camera_front: int
    camera_back: int
    color: str
    price: float
    release_date: date
    is_available: bool
    class Config: # Lors des réponses, nous avons souvant à utiliser les données sortie de notre database. La Config ORM nous permet de "choisir" les columnes à montrer. 
        orm_mode= True

class Customer_POST_Body (BaseModel):
    customerEmail:str
    customerPassword: str

class Customer_response (BaseModel): 
    id: int
    email:str
    create_at: datetime
    # not sending the password
    class Config: # Importante pour la traduction ORM -> DTO
        orm_mode= True      