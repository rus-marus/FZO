from flask_table import Table, Col, LinkCol

class Results(Table):
    id = Col(name='id', show=False)
    fam = Col(name='Фамилия')
    name = Col('Имя')
    father_name = Col('Отчество')
    date = Col('Дата рождения')
    rank = Col('Звание')
    edit = LinkCol('Изменить', 'edit', url_kwargs=dict(id='id'))