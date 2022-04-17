from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.api_routers import api_router
from db.init_db import database



origins = [
    "http://localhost",
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(api_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
