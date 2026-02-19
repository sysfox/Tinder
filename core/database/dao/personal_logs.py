from core.database.dao.base import BaseDAO
from core.database.orm.models.personal_logs import PersonalLog


class PersonalLogsDAO(BaseDAO):
    """personal_logs 表的数据访问对象。"""

    MODEL = PersonalLog
