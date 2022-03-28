from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..dependencies import authenticate_token, get_session
from ..models import Item, ItemBase

router = APIRouter()


@router.post(
    "/users/{user_id}/items/",
    dependencies=[Depends(authenticate_token)],
)
def create_item_for_user(
    user_id: int, item: ItemBase, session: Session = Depends(get_session)
):
    db_item = Item.from_orm(item, update={"user_id": user_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.get("/items/")
def read_items(session: Session = Depends(get_session)):
    items = session.exec(select(Item)).all()
    return items

