""" from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

##Manera usuarios e item
#cada usuario tiene sus items

class Item(BaseModel):
    title: str  #titulo
    description: Optional[str] = None #descripcion 


class User(BaseModel):
    username: str #Usuario (string)


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://fastapiworkshop.yaquelinehoyos.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/users/")
def create_user(user: User):
    return user


@app.get("/users/")
def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"id": user_id, "username": "Pickle Rick"}


@app.post("/users/{user_id}/items/")
def create_item_for_user(user_id: int, item: Item):
    return item


@app.get("/items/")
def read_items():
    return [
        {"title": "Portal Gun", "description": "A gun that shoots portals"},
        {"title": "Towel"},
    ] """

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from . import db, models
from .api import items, users


def create_db_and_tables():
    assert models, "Models should be imported so SQLModel has them registered"
    SQLModel.metadata.create_all(db.engine)


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://fastapiworkshop.yaquelinehoyos.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(items.router)


@app.on_event("startup")
def startup_event():
    create_db_and_tables()
