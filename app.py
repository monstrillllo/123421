from flask import Flask, g, render_template, request, flash, abort, jsonify
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
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(x):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/api/v1.0/films', methods=['POST'])
def add_film():
    db = get_db()
    dbase = FDataBase(db)

    if not request.json or 'title' not in request.json \
            or 'genre' not in request.json or 'short_review' not in request.json:
        abort(400)

    new_film = {
        'title': request.json['title'],
        'genre': request.json['genre'],
        'short_review': request.json['short_review']
    }
    dbase.add_film(new_film['title'], new_film['genre'], new_film['short_review'])
    # if not res:
    #     flash('Ошибка при добавлениии фильма', category='error')
    # else:
    #     flash('Фильм был успешно добавлен', category='success')
    return jsonify({'new_film': new_film}), 201


@app.route('/api/v1.0/films/<int:id_film>', methods=["GET"])
def get_film(id_film):
    db = get_db()
    dbase = FDataBase(db)
    title, genre, short_review = dbase.get_film(id_film)
    if not title:
        abort(404)
    film = {
        'title': title,
        'genre': genre,
        'short_review': short_review
    }

    # return render_template('film.html', menu=dbase.get_menu(), title=title, genre=genre, short_review=short_review)
    return jsonify(film)


@app.route('/api/v1.0/films', methods=["GET"])
def get_film_list():
    db = get_db()
    dbase = FDataBase(db)
    # return render_template('film_list.html', menu=dbase.get_menu(), title="Список фильмов",
    #                        film_list=dbase.get_film_list())
    return jsonify(dbase.get_film_list())


@app.route('/api/v1.0/films/<int:id_film>', methods=['DELETE'])
def delete_film(id_film):
    db = get_db()
    dbase = FDataBase(db)


    res = dbase.delete_film(id_film)

    return jsonify({'result': res})


@app.route('/api/v1.0/films/<int:id_film>', methods=['PUT'])
def change_film(id_film):
    db = get_db()
    dbase = FDataBase(db)

    # if request.method == "POST":
    #     if len(request.form['title']) >= 4 and len(request.form['genre']) >= 4 and \
    #             len(request.form['short_review']) >= 5 and len(request.form['id']) >= 1:
    #         res = dbase.change_film(request.form['id'], request.form['title'], request.form['genre'],
    #                                 request.form['short_review'])
    #         if not res:
    #             flash('Ошибка при изменении фильма', category='error')
    #         else:
    #             flash('Фильм был успешно изменен', category='success')

    res = dbase.change_film(id_film, request.json['title'], request.json['genre'], request.json['short_review'])

    return jsonify({'result': res})


if __name__ == '__main__':
    app.run(debug=True)
