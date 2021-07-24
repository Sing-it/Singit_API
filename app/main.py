from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI()


@app.get("/")
async def test():
    return {"message": "Server Listening"}


app.include_router(api_router)
