from core.database.dao.base import BaseDAO
from core.database.orm.models.tags import Tag


class TagsDAO(BaseDAO):
    """tags 表的数据访问对象。"""

    MODEL = Tag
