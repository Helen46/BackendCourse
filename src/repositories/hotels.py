from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepositiry


class HotelsRepositories(BaseRepositiry):
    model = HotelsOrm
