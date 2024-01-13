from mysql import connector
from time import sleep

db = connector.connect(
    host='smart-garden-db',
    user='root',
    password='test',
    database='smart_garden'
)
