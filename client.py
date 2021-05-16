from flask import Flask, render_template, request, redirect, abort
import requests

app = Flask(__name__)

films_url = 'http://127.0.0.1:5000/api/v1.0/films'


@app.route('/')
def hello():
    return 'HELLO'


@app.route('/films/add_film', methods=['GET', 'POST'])
def add_film():
    if request.method == 'GET':
        return render_template('add_film.html')

    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        short_review = request.form['short_review']
        data = {
            'title': title,
            'genre': genre,
            'short_review': short_review
        }
        requests.post(films_url, json=data)
        return redirect('/films')


@app.route('/films')
def RetrieveListFilm():
    r = requests.get(films_url)
    resp = r.json()
    return render_template('film_list.html', films=resp)


@app.route('/films/<int:id>')
def RetrieveFilm(id):
    r = requests.get(films_url + '/' + str(id))
    film = r.json()
    if film:
        return render_template('film.html', film=film)
    return f"Film with id ={id} Doesn't exist"


@app.route('/films/<int:id>/change_film', methods=['GET', 'POST'])
def change_film(id):
    r = requests.get(films_url + '/' + str(id))
    film = r.json()
    if request.method == 'POST':
        if film:
            new_title = request.form['title']
            new_genre = request.form['genre']
            new_short_review = request.form['short_review']
            data = {
                'title': new_title,
                'genre': new_genre,
                'short_review': new_short_review
            }
            requests.put(films_url + '/' + str(id), json=data)
            return redirect(f'/films/{id}')
        return f"Film with id = {id} Doesnt exist"

    return render_template('change_film.html', film=film)


@app.route('/films/<int:id>/delete', methods=['GET', 'POST'])
def delete_country(id):
    if request.method == 'POST':
        requests.delete(films_url + '/' + str(id))
        return redirect('/films')

    return render_template('delete_film.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5001)
