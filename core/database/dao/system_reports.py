from core.database.dao.base import BaseDAO
from core.database.orm.models.system_reports import SystemReport


class SystemReportsDAO(BaseDAO):
    """system_reports 表的数据访问对象。"""

    MODEL = SystemReport
