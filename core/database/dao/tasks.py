from core.database.dao.base import BaseDAO
from core.database.orm.models.tasks import Task


class TasksDAO(BaseDAO):
    """tasks 表的数据访问对象。"""

    MODEL = Task
