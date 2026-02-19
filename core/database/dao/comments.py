from core.database.dao.base import BaseDAO
from core.database.orm.models.comments import Comment


class CommentsDAO(BaseDAO):
    """comments 表的数据访问对象。"""

    MODEL = Comment
