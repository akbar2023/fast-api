from sqlalchemy import TIMESTAMP, Boolean, Column, Date, ForeignKey, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

# Class de base pour créer les models
Base= declarative_base()

# ORM Smartphones 
class Smartphones(Base):
    __tablename__= "smartphone"
    id = Column(Integer, primary_key=True, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    ram = Column(Integer, nullable=False)
    camera_front = Column(Integer, nullable=False)
    camera_back = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    release_date = Column(Date, nullable=False)
    is_available = Column(Boolean, nullable=True, server_default='TRUE') # valeur par default à True

class Users(Base):
    __tablename__="user"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, server_default='FALSE')
    create_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')  

class Transactions(Base):
    __tablename__="transaction"
    id= Column(Integer, primary_key=True, nullable=False)
    user_id= Column(Integer, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)  # Les Foreign Keys sont basés sur les clé principales des autres tables mais ce n'est pas obligatoire
    smartphone_id = Column(Integer, ForeignKey("smartphone.id", ondelete="RESTRICT"), nullable=False) # ondelete permet de choisir la cascade d'action suite à la suppression (supprimer une transation, doit-elle suppimer le customer ou le produit?)
    transaction_date=Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")