from os import getenv
from mysql import connector


def init_db(app):
    app.db = connector.connect(
        host=getenv('MYSQL_DB_HOSTNAME'),
        user=getenv('MYSQL_USER'),
        password=getenv('MYSQL_ROOT_PASSWORD'),
        database=getenv('MYSQL_DATABASE_NAME')
    )
