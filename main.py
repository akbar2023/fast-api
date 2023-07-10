
from fastapi import FastAPI

# Documentation
from documentation.description import api_description
from documentation.tags import tags_metadata


# Database 
from classes.database import database_engine 
import classes.models_orm # Import des ORM

#Import des routers
import routers.router_smartphones, routers.router_users, routers.router_transactions, routers.router_auth

# Créer les tables si elles ne sont pas présente dans la DB
classes.models_orm.Base.metadata.create_all(bind=database_engine)





#Lancement de l'API
app= FastAPI( 
    title="Smartphones API",
    description=api_description,
    openapi_tags=tags_metadata # tagsmetadata definit au dessus
    )

@app.get("/")
async def root(): 
    return {
        "message": "Bonjour!"
    }

# Ajouter les routers dédiés
app.include_router(routers.router_smartphones.router)
app.include_router(routers.router_users.router)
app.include_router(routers.router_transactions.router)
app.include_router(routers.router_auth.router)