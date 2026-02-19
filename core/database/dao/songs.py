from core.database.dao.base import BaseDAO
from core.database.orm.models.songs import Song


class SongsDAO(BaseDAO):
    """songs 表的数据访问对象。"""

    MODEL = Song
