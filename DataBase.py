import psycopg2.extras

class DataBase:
    def __init__(self,db):
        self.__db = db
        self.__cur = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)


    # Сделать универсальный метод, который будет выдавать res по sql запросу, который передается в функцию, и 1 или 0 для выбора fetchone или fetchall
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
    def getAbiturient(self, id):
        try:
            self.__cur.execute(f"SELECT * FROM abiturients WHERE id = {id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                return False

            return res
        except:
            print("Ошибка получения данных из БД ")

        return False
    def getInfo(self):
        try:
            self.__cur.execute(f"SELECT * FROM abiturients")
            res = self.__cur.fetchall()
            if not res:
                print("Таблица абитуриентов пустая")
                return False

            return res
        except:
            print("Ошибка получения данных из БД ")

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