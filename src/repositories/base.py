from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
       query = select(self.model)
       result = await self.session.execute(query)
       return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
       query = select(self.model).filter_by(**filter_by)
       result = await self.session.execute(query)
       return result.scalars().one_or_none()

    async def add_data(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)
        return result.scalars().one()

    async def update_data(self, data: BaseModel, is_patch, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=is_patch))
        )
        await self.session.execute(update_stmt)

    async def delete_data(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
