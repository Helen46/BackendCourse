from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.comforts import ComfortAdd

router = APIRouter(prefix="/comforts", tags=["Удобства"])


@router.get("", summary="Получение всех удобств")
async def get_comforts(db: DBDep):
    return await db.comforts.get_all()


@router.post("", summary="Добавление удобства")
async def create_comfort( db: DBDep, comfort_data: ComfortAdd = Body()):
    comfort = await db.comforts.add_data(comfort_data)
    await db.commit()

    return {"status": "OK", "data": comfort}
