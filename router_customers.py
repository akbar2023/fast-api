from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_cursor
import models_orm, schemas_dto

router = APIRouter(
    prefix='/customers'
)


@router.get('', response_model=list[schemas_dto.Customer_response])
async def get_all_customers(cursor: Session = Depends(database.get_cursor)):
    all_customers = cursor.query(models_orm.Customers).all()
    return all_customers