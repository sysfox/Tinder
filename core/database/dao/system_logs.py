from core.database.dao.base import BaseDAO
from core.database.orm.models.system_logs import SystemLog


class SystemLogsDAO(BaseDAO):
    """system_logs 表的数据访问对象。"""

    MODEL = SystemLog
