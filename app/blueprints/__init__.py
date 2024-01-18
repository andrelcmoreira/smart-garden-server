from mysql import connector
from os import getenv


db = connector.connect(
    host='smart-garden-db',
    user='root',
    password=getenv('MYSQL_ROOT_PASSWORD'),
    database='smart_garden'
)
