from flask import Flask, render_template, url_for, request, flash, session, redirect, g
from flask_login import LoginManager, login_user, login_required, logout_user, current_user # pip install flask-login 
import psycopg2
from UserLogin import UserLogin
from DataBase import DataBase

app = Flask(__name__)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = "2738a590569501f38f14871dbb6f9129a323deac4bc501f2cd"
login_manager.login_view = 'login'
login_manager.login_message = ""

def connect_db():
    conn = psycopg2.connect(
        host="127.0.0.1",
            port="5432",
                database='FZO',
                    user="jigan",
                        password="12345")
    return conn


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)

def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    datab = get_db()
    dbase = DataBase(datab)


@app.teardown_appcontext 
def close_db(eror):
    '''Закрываем соединение с БД, когда происходит уничтожение контекста приложения, 
    т.е. в момент завершения обработки запроса (если оно было установлено)'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


# нужно уходить от использования одной страницы,т.к. код всего сайта будет забит в одном методе - а это шляпа
# тогда сделаем основную страницу - главным меню, но если пользователь не авторизован, то перекидываем его на /login

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for("login"))
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == "POST":
        user = dbase.getUserByLogin(request.form['login'])
        if user and request.form['password'] == '123':
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            # return redirect(request.args.get("next") or url_for("menu"))
            return redirect(url_for('index'))
        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html", title='Авторизация в системе')


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == "POST":
         if request.form['menu'] == "Выйти":
            logout_user()
            return redirect(url_for("login"))
         elif request.form['menu'] == "Просмотр анкет":
            return  redirect(url_for('abiturients'))
    return render_template("menu.html", title='Меню')

@app.route('/abiturients', methods=['POST', 'GET'])
@login_required
def abiturients():
    return render_template('view.html')


@app.route('/abiturient/<int:id>', methods=['GET', 'POST'])
@login_required
def edit():
    abiturient = dbase.getAbiturient()
    return render_template('abiturient.html', abiturient = abiturient)

@app.route('/api/data')
@login_required
def data():
    id = session['_user_id']
    complect = dbase.getComplect(id=id)['complect']
    abiturients_data = dbase.getInfo(complect)
    for ab in range(0, len(abiturients_data),+1):
        abiturients_data[ab]['url'] = '<a href="/abiturient/' + str(abiturients_data[ab]['id_abiturient']) + '">Изменить</a></td>'

    return {'data': abiturients_data}

if __name__ == "__main__":
    app.run(debug=True)