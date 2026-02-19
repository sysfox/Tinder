from core.database.dao.base import BaseDAO
from core.database.orm.models.favourites import Favourite


class FavouritesDAO(BaseDAO):
    """favourites 表的数据访问对象。"""

    MODEL = Favourite
