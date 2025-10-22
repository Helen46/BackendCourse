from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotel", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров отеля")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2025-10-01"),
        date_to: date = Query(example="2025-10-20"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение одного номера")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms", summary="Добавление номера")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Hotel Resort 5 Stars",
        "value": {
            "title": "Стандарт",
            "description": "Номер для двоих",
            "price": 3000,
            "quantity": 5,
        }
    },
    "2": {
        "summary": "Hotel Beach Resort",
        "value": {
            "title": "Люкс",
            "description": "Шикарный номер с гостиной, балконом и джакузи",
            "price": 20000,
            "quantity": 3,
        }

    }

})
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.get_one_or_none(id=hotel_id)
    room = await db.rooms.add_data(_room_data)

    await db.commit()
    return{"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновление данных номера")
async def edit_room(hotel_id: int, room_id: int, db: DBDep, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.update_data(
            _room_data,
            is_patch=True,
            hotel_id=hotel_id,
            id=room_id
        )
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление номера")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.update_data(
        _room_data,
        is_patch=True,
        hotel_id=hotel_id,
        id=room_id
    )
    await db.commit()
    return {"status": "OK"}



@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete_data(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}