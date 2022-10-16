import psycopg2.extras

class DataBase:
    def __init__(self,db):
        self.__db = db
        self.__cur = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)


    def get_User(self, user_id):
        try:
            self.cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except:
            print('Ошибка получения данных из БД')

        return False

    def getUserByLogin(self, login):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE login = '{login}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except:
            print("Ошибка получения данных из БД ")

        return False