from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepositiry


class RoomsRepositories(BaseRepositiry):
    model = RoomsOrm
