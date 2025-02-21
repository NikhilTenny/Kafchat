import asyncio
from typing import Union
from fastapi import FastAPI
from src.authentication.routes import router as auth_router
from src.chat.routes import router as chat_router, listen_to_redis
from src.database import create_db_and_tables

import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Doc-Assist API"
)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

    
    
@app.on_event("startup")
async def startup():
    create_db_and_tables()
    asyncio.create_task(listen_to_redis())

   
    
    

app.include_router(auth_router)
app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, or specify a list of allowed domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    


