from fastapi import FastAPI
app = FastAPI() # var name of the app

@app.get("/")
async def root(): 
    return {"message": "Bonjour !"}