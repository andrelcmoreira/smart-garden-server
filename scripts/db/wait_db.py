from mysql import connector as conn
from sys import exit


def main():
    try:
        db = conn.connect(host="smart-garden-db",
                          user="root",
                          password="test")
        db.close()
    except conn.errors.DatabaseError:
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
