from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
       query = select(self.model).filter(*filter).filter_by(**filter_by)
       result = await self.session.execute(query)
       # приводим результат к pydantic schema а не к объекту БД
       return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
       return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
       query = select(self.model).filter_by(**filter_by)
       result = await self.session.execute(query)
       model = result.scalars().one_or_none()
       if model is None:
           return None
       return self.schema.model_validate(model, from_attributes=True)

    async def add_data(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

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
