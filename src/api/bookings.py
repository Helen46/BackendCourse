from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep, PaginationDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получение всех бронирований")
async def get_bookings(pagination: PaginationDep, db: DBDep,):
    per_page = pagination.per_page or 5
    return await db.bookings.get_all(
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/me", summary="Получение своих бронирований")
async def get_my_bookings(user_id: UserIdDep,db: DBDep):
    user = await db.users.get_one_or_none(id=user_id)
    return await db.bookings.get_filtered(user_id=user.id)


@router.post("", summary="Добавление бронирования")
async def create_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest = Body()):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add_data(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
