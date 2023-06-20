from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date

import psycopg2
from psycopg2.extras import RealDictCursor

# Connexion DB
"""
postgres://
akbar_render
:
yHsSMaPMloDONSY7QSXrKyerN63W2M6G
@
dpg-ci8rn3p8g3n3vm6clsv0-a.frankfurt-postgres.render.com
/
mobiles
"""
connexion = psycopg2.connect(
    host="dpg-ci8rn3p8g3n3vm6clsv0-a.frankfurt-postgres.render.com", 
    database="mobiles",
    user="akbar_render",
    password="yHsSMaPMloDONSY7QSXrKyerN63W2M6G",
    cursor_factory=RealDictCursor
    )

cursor = connexion.cursor()


# Description
api_description = description = """
Watch API helps you do awesome stuff.

## Users
*
*
*

## Products

You will be able to : 
* Create new products.
* Get products list.
* Create products
* Update

"""

# Liste des tags utilisés dans la doc
tags_metadata = [
    {
        "name": "Products",
        "description": "Manage Products. So _Fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com"
        }
    },
    {
        "name": "Users",
        "description": "Manage Users. So _Fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com"
        }
    }
]


app = FastAPI(
    title= "Mobile API",
    description= api_description,
    openapi_tags=tags_metadata #tagmetadata est defini au dessus
) # var name of the app

class Mobile(BaseModel): 
    brand: str
    storage: int
    ram: int
    color: str
    price: float
    release_date: date
    is_available: bool


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
        },
        {
            "Model": "Xiaomi 11",
            "Brand" : "Mi",
            "Storage": "128GB",
            "Camera": "48 MPx",
            "Price" : "900"
        }
    ]

class User(BaseModel):
    username: str
    password: str

usersList = [
    {
        "username": "akbar-khan",
        "password": "0000"
    },
    {
        "username": "jhon-doe",
        "password": "0000"
    },
    {
        "username": "Frank-Dubois",
        "password": "0000"
    }
]

    


@app.get("/")
async def root(): 
    return {
        "message": "Bonjour!"
    }

@app.get("/products", tags=["Products"])
async def getProducts():
    cursor.execute("SELECT * FROM mobilephones")
    mobiles = cursor.fetchall()
    return {
        "products": mobiles,
        "limit": 10,
        "total": 20,
        "skip": 0
    }

@app.get("/products/{product_id}", tags=["Products"])
async def get_product(product_id: int, response: Response):
    try:
        cursor.execute(f"SELECT * FROM mobilephones WHERE phone_id ={product_id}")
        corresponding_product = cursor.fetchone()
        if(corresponding_product):
            return corresponding_product
        else:
            raise HTTPException (
            status.HTTP_404_NOT_FOUND,
            detail= "Product not found"
        )
    except:
        raise HTTPException (
            status.HTTP_404_NOT_FOUND,
            detail= "Product not found"
        )


@app.post("/products", tags=["Products"])
async def addProducts(payload: Mobile, response: Response):
    insert_query = """
        INSERT INTO mobilephones (brand, storage, ram, color, price, release_date, is_available)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING *
    """
    data = (
        payload.brand,
        payload.storage,
        payload.ram,
        payload.color,
        payload.price,
        payload.release_date.strftime('%Y-%m-%d'),  # Format the date as string
        payload.is_available
    )

    cursor.execute(insert_query, data)
    connexion.commit()
    response.status_code = status.HTTP_201_CREATED
    return {
        "message": f"{payload.brand} added successfully"
    }


# DELETE :
@app.delete("/products/{product_id}", tags=["Products"])
async def deleteProduct(product_id: int, response: Response):
    try:
        delete_query = "DELETE FROM mobilephones WHERE phone_id=%s"

        data = str(product_id)
        cursor.execute(delete_query, data)
        connexion.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail = "product not found"
        )
    
@app.put("/products/{product_id}", tags=["Products"])
async def replaceProduct(product_id: int, payload: Mobile, response: Response):
    try:
        update_query = """
            UPDATE mobilephones SET brand=%s, storage=%s, ram=%s, color=%s, price=%s, 
            release_date=%s, is_available=%s WHERE phone_id=%s
        """
        data = (
            payload.brand,
            payload.storage,
            payload.ram,
            payload.color,
            payload.price,
            payload.release_date,
            payload.is_available,
            product_id
        ) 
        cursor.execute(update_query, data)
        connexion.commit()
        return {"message": f"updated successfully: {payload.brand}"}
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Product not found"
        )



# USERS

@app.get("/users", tags=["Users"])
async def getUsers():
    return usersList

@app.get("/users/{user_id}", tags=["Users"])
async def get_product(user_id: int, response: Response):
    try:
        corresponding_user = usersList[user_id -1]
        return corresponding_user
    except:
        raise HTTPException (
            status.HTTP_404_NOT_FOUND,
            detail= "User not found"
        )
    
@app.post("/users", tags=["Users"])
async def addProducts(payload: User, response: Response):
    print(payload.username)
    usersList.append(payload.dict())
    response.status_code = status.HTTP_201_CREATED
    return {
        "message": f"{payload.username} added successfully"
    }


# DELETE :
@app.delete("/users/{user_id}", tags=["Users"])
async def deleteProduct(user_id: int, response: Response):
    try:
        usersList.pop(user_id -1)
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail = "user not found"
        )
    
@app.put("/users/{user_id}", tags=["Users"])
async def replaceProduct(user_id: int, payload: User, response: Response):
    try:
        usersList[user_id -1] = payload.dict()
        return {"message": f"updated successfully: {payload.username}"}
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Product not found"
        )