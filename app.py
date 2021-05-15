from flask import Flask, g, render_template, request, flash, abort
import sqlite3
import os

from FDataBase import FDataBase

DATABASE = '/tmp/server_db.db'
DEBUG = True
SECRET_KEY = 'wfuwhijofwjepfwjefwlekf'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'server_db.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    # conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """ Функция для создания таблиц"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """соеденение с дб если оно не установлено"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(x):
    """закрытие соединения если оно есть"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
@app.route('/index')
def index():
    db = get_db()
    dbase = FDataBase(db)
    # print(dbase.get_menu())
    return render_template('index.html', menu=dbase.get_menu())


@app.route('/add_film', methods=['GET', 'POST'])
def add_film():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['title']) >= 4 and len(request.form['genre']) >=4 and len(request.form['short_review']) >= 5:
            res = dbase.add_film(request.form['title'], request.form['genre'], request.form['short_review'])
            if not res:
                flash('Ошибка при добавлениии фильма', category='error')
            else:
                flash('Фильм был успешно добавлен', category='success')
    return render_template('add_film.html', menu=dbase.get_menu(), title='Добавление фильма')


@app.route('/film_list/<int:id_film>')
def film(id_film):
    db = get_db()
    dbase = FDataBase(db)
    title, genre, short_review = dbase.get_film(id_film)
    if not title:
        abort(404)

    return render_template('film.html', menu=dbase.get_menu(), title=title, genre=genre, short_review=short_review)


@app.route('/film_list')
def film_list():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('film_list.html', menu=dbase.get_menu(), title="Список фильмов",
                           film_list=dbase.get_film_list())


@app.route('/delete_film', methods=['GET', 'POST'])
def delete_film():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['id']) != 0:
            res = dbase.delete_film(request.form['id'])
            if not res:
                flash('Ошибка при удалении фильма', category='error')
            else:
                flash('Фильм был успешно удален', category='success')
    return render_template('delete_film.html', menu=dbase.get_menu(), title='Удаление фильма')


@app.route('/change_film', methods=['GET', 'POST'])
def change_film():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['title']) >= 4 and len(request.form['genre']) >= 4 and\
                len(request.form['short_review']) >= 5 and len(request.form['id']) >= 1:
            res = dbase.change_film(request.form['id'], request.form['title'], request.form['genre'],
                                    request.form['short_review'])
            if not res:
                flash('Ошибка при изменении фильма', category='error')
            else:
                flash('Фильм был успешно изменен', category='success')
    return render_template('change_film.html', menu=dbase.get_menu(), title='Изменение фильма')


if __name__ == '__main__':
    app.run(debug=True)
