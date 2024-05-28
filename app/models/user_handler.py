from models.database_mgr import DatabaseMgr
from models.entities.user import User
from models.table_handler import TableHandler


class UserHandler(TableHandler):

    '''
    Handler for user table.

    '''

    @staticmethod
    def get(user):
        db = DatabaseMgr.get_db()

        with db.cursor() as cursor:
            cursor.execute(f'select * from users where username = "{user}"')

            ret = cursor.fetchone()
            if not ret:
                return None

        return User(username=ret[1], passwd=ret[2])
