from datetime import date

from sqlalchemy import select, func

from src.database import engine
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            hotel_id,

    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))