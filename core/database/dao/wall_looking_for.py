from core.database.dao.base import BaseDAO
from core.database.orm.models.wall_looking_for import WallLookingFor


class WallLookingForDAO(BaseDAO):
    """wall_looking_for 表的数据访问对象。"""

    MODEL = WallLookingFor
