from typing import Union
from fastapi import FastAPI
from src.authentication.routes import router as auth_router
from src.chat.routes import router as chat_router
from src.database import create_db_and_tables
import uvicorn

app = FastAPI(
    title="Doc-Assist API"
)


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

    
    
@app.on_event("startup")
async def startup():
    create_db_and_tables()
    # redis_connection = redis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    # await FastAPILimiter.init(redis_connection)
   
    

app.include_router(auth_router)
app.include_router(chat_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    


