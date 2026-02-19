from core.database.dao.base import BaseDAO
from core.database.orm.models.song_arrangements import SongArrangement


class SongArrangementsDAO(BaseDAO):
    """song_arrangements 表的数据访问对象。"""

    MODEL = SongArrangement
