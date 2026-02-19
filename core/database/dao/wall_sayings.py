from core.database.dao.base import BaseDAO
from core.database.orm.models.wall_sayings import WallSaying


class WallSayingsDAO(BaseDAO):
    """wall_sayings 表的数据访问对象。"""

    MODEL = WallSaying
