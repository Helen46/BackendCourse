from datetime import date

from fastapi import Query, APIRouter, Body

from src.database import engine

from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение списка отелей")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(example="2025-10-01"),
        date_to: date = Query(example="2025-10-20"),

):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/{hotel_id}", summary="Получение одного отеля")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("", summary="Добавление отеля",)
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    "1": {
        "summary": "Sochi",
        "value": {
            "title": "Hotel Resort 5 Stars",
            "location": "Sochi, Beach St. 1",
        }
    },
    "2": {
        "summary": "Dubai",
        "value": {
            "title": "Hotel Resort 5 Stars",
            "location": "Dubai, Sheikh St. 2",
        }
    }
})
):
    hotel = await db.hotels.add_data(hotel_data)
    # проверка данных, которые отправляются в БД
    # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))

    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Обновление данных об отеле")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.update_data(hotel_data, is_patch=False, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPATCH,

):
    await db.hotels.update_data(hotel_data, is_patch=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete_data(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
