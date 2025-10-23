from sqlalchemy import select, delete, insert

from src.models.comforts import ComfortsOrm, RoomsComfortsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import ComfortDataMapper, RoomComfortDataMapper


class ComfortsRepository(BaseRepository):
    model = ComfortsOrm
    mapper = ComfortDataMapper


class RoomsComfortsRepository(BaseRepository):
    model = RoomsComfortsOrm
    mapper = RoomComfortDataMapper

    async def set_room_comforts(self, room_id: int, comforts_ids: list[int]) -> None:
        get_current_comforts_ids_query = (
            select(self.model.comfort_id)
            .filter_by(room_id=room_id)
        )
        res = await self.session.execute(get_current_comforts_ids_query)
        current_comforts_ids: list[int] = res.scalars().all()
        ids_to_delete: list[int] = list(set(current_comforts_ids) - set(comforts_ids))
        ids_to_insert: list[int] = list(set(comforts_ids) - set(current_comforts_ids))

        if ids_to_delete:
            delete_m2m_comforts_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.comfort_id.in_(ids_to_delete),
                )
            )
            await self.session.execute(delete_m2m_comforts_stmt)

        if ids_to_insert:
            insert_m2m_comforts_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "comfort_id": c_id} for c_id in ids_to_insert])
            )
            await self.session.execute(insert_m2m_comforts_stmt)
