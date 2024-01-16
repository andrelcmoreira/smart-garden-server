from mysql import connector

db = connector.connect(
    host='smart-garden-db',
    user='root',
    password='test',
    database='smart_garden'
)