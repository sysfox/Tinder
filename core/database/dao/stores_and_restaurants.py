from core.database.dao.base import BaseDAO
from core.database.orm.models.stores_and_restaurants import StoreOrRestaurant


class StoresAndRestaurantsDAO(BaseDAO):
    """stores_and_restaurants 表的数据访问对象。"""

    MODEL = StoreOrRestaurant
