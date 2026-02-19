from core.database.dao.base import BaseDAO
from core.database.orm.models.vote import Vote


class VoteDAO(BaseDAO):
    """vote 表的数据访问对象。"""

    MODEL = Vote
