import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = """SELECT * FROM mainmenu"""
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                result = []
                for m in res:
                    result.append({
                        'title': m[1],
                        'url': m[2]
                    })
                return result
        except:
            print("ошибка чтения db")
        return []

    def add_film(self, title, genre, short_review):
        try:
            self.__cur.execute("INSERT INTO film_list VALUES (NULL, ?,  ?, ?)", (title, genre, short_review))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления фильма в db " + str(e))
            return False

        return True

    def get_film(self, filmId):
        try:
            self.__cur.execute(f"SELECT title, genre, short_review FROM film_list WHERE id={filmId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения из db" + str(e))

        return False, False

    def get_film_list(self):
        try:
            self.__cur.execute("SELECT id, title FROM film_list ORDER BY id")
            res = self.__cur.fetchall()
            if res:
                result = []
                for f in res:
                    result.append({
                        'id': f[0],
                        'title': f[1]
                    })
                return result
        except sqlite3.Error as e:
            print("Ошибка получения списка фильмов из db " + str(e))
        return []

    def delete_film(self, film_id):
        try:
            self.__cur.execute(f"DELETE FROM film_list WHERE id={film_id}")
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления фильма в db " + str(e))
            return False

        return True

    def change_film(self, film_id, title, genre, short_review):
        try:
            query = """UPDATE film_list SET title=?, genre=?, short_review=? WHERE id=?"""
            data = (title, genre, short_review, film_id)
            self.__cur.execute(query, data)
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка изменения фильма в db " + str(e))
            return False

        return True


