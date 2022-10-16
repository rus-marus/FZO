from flask_login import UserMixin

class UserLogin(UserMixin):

    def fromDB(self, user_id, db): #используется при создании декоратора load_user, чтобы передать данные из декоратора в UserLogin
        self.__user = db.get_User(user_id) #формируем __user и присваиваем ему информацию по текущему пользователю
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])