from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm
import utilities
from sqlalchemy.exc import IntegrityError

# Ajout du schema Oauth sur un endpoint précis (petit cadenas)
# Le boutton "Authorize" ouvre un formulaire en popup pour capturer les credentials
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


router= APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

# Get all transactions filtered with user_id
@router.get('')
async def list_transactions(
    token: Annotated[str, Depends(oauth2_scheme)], 
    cursor: Session = Depends(get_cursor)):
        # Le décodage du token permet de récupérer l'identifiant du customer
        decoded_user_id = utilities.decode_token(token)
        all_transactions = cursor.query(models_orm.Transactions).filter(models_orm.Transactions.user_id == decoded_user_id).all()
        return all_transactions # data format à ajuster cela besoin

# DTO pour récupérer le smartphone_id car le user_id est déjà dans le JWToken
class transaction_post(BaseModel):
    smartphone_id:int

@router.post('', status_code=status.HTTP_201_CREATED)
async def create_transaction(
    token: Annotated[str, Depends(oauth2_scheme)], # Sécurisation par Auth 
    payload:transaction_post,
    cursor: Session = Depends(get_cursor)
    ):
    decoded_user_id = utilities.decode_token(token)
    new_transaction= models_orm.Transactions(user_id=decoded_user_id, smartphone_id=payload.smartphone_id)
    try : 
        cursor.add(new_transaction)
        cursor.commit()
        cursor.refresh(new_transaction)
        return {'message' : f'New transaction added on {new_transaction.transaction_date} with id:{new_transaction.id}' }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='the given product does not exist'
        )