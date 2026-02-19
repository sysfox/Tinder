from core.database.dao.base import BaseDAO
from core.database.orm.models.users import User


class UsersDAO(BaseDAO):
    """users 表的数据访问对象。"""

    MODEL = User
