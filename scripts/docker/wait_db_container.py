from mysql import connector as conn
from os import getenv
from sys import exit


def main():
    try:
        db = conn.connect(host=getenv('MYSQL_DB_HOSTNAME'),
                          user=getenv('MYSQL_USER'),
                          password=getenv('MYSQL_ROOT_PASSWORD'))
        db.close()
    except conn.errors.DatabaseError:
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
