# 导入pgsql
import psycopg2
from psycopg2 import sql
import os
from datetime import datetime
import dotenv

# 连接数据库
# 从环境变量获取 DATABASE_URL
def connect_to_database():
    """连接到数据库"""
    # 如果.env文件存在
    if os.path.exists('.env'):
        dotenv.load_dotenv('.env')
        url = os.getenv('DATABASE_URL')
    else:
        # 否则从环境变量获取 DATABASE_URL
        url = os.getenv('DATABASE_URL')
    
    try:
        conn = psycopg2.connect(url)
        print("✅ 数据库连接成功")
        return conn
    except psycopg2.Error as e:
        print(f"❌ 数据库连接失败: {e}")
        raise

# 创建migration_history表
def create_migration_history_table(conn):
    """创建migration_history表来记录迁移历史"""
    cursor = conn.cursor()
    
    try:
        # 创建migration_history表
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS migration_history (
            id SERIAL PRIMARY KEY,
            migration_name VARCHAR(255) NOT NULL UNIQUE,
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(50) DEFAULT 'success',
            error_message TEXT
        );
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        print("✅ migration_history 表创建成功")
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ 创建表失败: {e}")
        raise
    finally:
        cursor.close()

# 主函数
if __name__ == "__main__":
    try:
        # 连接数据库
        conn = connect_to_database()
        
        # 创建migration_history表
        create_migration_history_table(conn)
        
        # 关闭连接
        conn.close()
        print("✅ 数据库迁移完成，连接已关闭")
        
    except Exception as e:
        print(f"❌ 执行迁移时出错: {e}")
        exit(1)