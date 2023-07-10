
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm, schemas_dto
import utilities
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter(
    prefix='/smartphones',
    tags=['SmartPhones']
)

# Read
@router.get('')
async def get_smartphones(
    cursor: Session= Depends(get_cursor), 
    limit:int=10, offset:int=0):
    all_phones = cursor.query(models_orm.Smartphones).limit(limit).offset(offset).all() # Lancement de la requête
    products_count= cursor.query(func.count(models_orm.Smartphones.id)).scalar()
    return {
        "smartphones": all_phones,
        "limit": limit,
        "total": products_count,
        "skip":offset
    }


# Read by id
@router.get('/{phone_id}', response_model=schemas_dto.Smartphone_GETID_Response)
async def get_product(phone_id:int, cursor:Session= Depends(get_cursor)):
    corresponding_phone = cursor.query(models_orm.Smartphones).filter(models_orm.Smartphones.id == phone_id).first()
    if(corresponding_phone):  
        return corresponding_phone
    else:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding smartphone found with id : {phone_id}"
        )

# CREATE / POST 
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_phone(payload: schemas_dto.Smartphone_POST_Body, cursor:Session= Depends(get_cursor)):
    new_phone = models_orm.Smartphones(brand=payload.brand, 
                                       model=payload.model,
                                       ram=payload.ram,
                                       camera_front=payload.camera_front,
                                       camera_back=payload.camera_back,
                                       color=payload.color,
                                       price=payload.price,
                                       release_date=payload.release_date,
                                       is_available=payload.is_available,
                                       ) # build the insert
    cursor.add(new_phone) # Send the query
    cursor.commit() #Save the staged change
    cursor.refresh(new_phone)
    return {"message" : f"New Smartphone {new_phone.brand + ' ' + new_phone.model} added sucessfully with id: {new_phone.id}"} 


# DELETE (Only possible by admin)
@router.delete('/{phone_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_phone(phone_id: int, token: str = Depends(oauth2_scheme), cursor: Session = Depends(get_cursor)):
    decoded_user_id = utilities.decode_token(token)
    connected_user = cursor.query(models_orm.Users).filter(models_orm.Users.id == decoded_user_id).first()
    # Recherche si le produit existe
    corresponding_product = cursor.query(models_orm.Smartphones).filter(models_orm.Smartphones.id == phone_id)
    # Check if user is admin
    print(f'IS_ADMIN {connected_user.is_admin}')
    if not connected_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Method allowed for admin only'
        )
    if corresponding_product.first() and connected_user.is_admin:
        # Continue to delete
        corresponding_product.delete()  # supprime
        cursor.commit()  # commit the stated changes (changement latent)
        return
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding product with id: {phone_id}'
        )

# Update
@router.patch('/{phone_id}')
async def update_phone(phone_id: int, payload:schemas_dto.Smartphone_PATCH_Body, cursor:Session=Depends(get_cursor)):
    # trouver le produit correspodant
    corresponding_product = cursor.query(models_orm.Smartphones).filter(models_orm.Smartphones.id == phone_id)
    if(corresponding_product.first()):
        # mise à jour (quoi avec quelle valeur ?) Body -> DTO
        corresponding_product.update({'is_available':payload.is_available})
        cursor.commit()
        return corresponding_product.first()
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ne corresponding phone with id: {phone_id}'
        )