from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional


app = FastAPI() # var name of the app

class Mobile(BaseModel): 
    Model: str
    Brand: str
    Storage: str
    Camera: str
    Price: float
    available: bool = True
    rating: Optional[int]

products = [
            {
            "Model": "Iphone 14 pro max",
            "Brand" : "Apple",
            "Storage": "128GB",
            "Camera": "48 MPx",
            "Price" : "1329"
        },
        {
            "Model": "Galaxy S23",
            "Brand" : "Samsung",
            "Storage": "128GB",
            "Camera": "48 MPx",
            "Price" : "900"
        }
    ]



@app.get("/")
async def root(): 
    return {
        "message": "Bonjour!"
    }

@app.get("/products")
async def getProducts():
    return products

@app.get("/products/{product_id}")
async def get_product(product_id: int, response: Response):
    try:
        corresponding_product = products[product_id -1]
        return corresponding_product
    except:
        raise HTTPException (
            status.HTTP_404_NOT_FOUND,
            detail= "Product not found"
        )


@app.post("/products")
async def addProducts(payload: Mobile, response: Response):
    print(payload.Model)
    products.append(payload.dict())
    response.status_code = status.HTTP_201_CREATED
    return {
        "message": f"{payload.Model} added successfully"
    }