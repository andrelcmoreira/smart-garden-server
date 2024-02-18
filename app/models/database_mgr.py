from mysql import connector
from os import getenv


class DatabaseMgr:

    """Docstring for DatabaseMgr. """

    db = None

    @classmethod
    def init_db(cls):
        cls.db = connector.connect(
            host=getenv('MYSQL_DB_HOSTNAME'),
            user=getenv('MYSQL_USER'),
            password=getenv('MYSQL_ROOT_PASSWORD'),
            database=getenv('MYSQL_DATABASE_NAME')
        )

    @classmethod
    def get_db(cls):
        return cls.db
