from flask import Flask
from flask import render_template, request, redirect, url_for, g
import sqlite3


app = Flask(__name__)

DATABASE = "data.db"


def get_db():
    db = getattr(g, '_database', None)  # присваиваем переменной db значение переменной _database из g, если его нет, то None
    if db is None:
        db = g._database = sqlite3.connect(DATABASE) # присваиваем переменной _database и db соединение с базой данных
        db.row_factory = sqlite3.Row # Использование row_factory позволяет брать метаданные из запроса и обращаться в итоге к результату, например по имени столбца.
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args) # Делаем SELECT запрос к базе данных, используя обычный SQL-синтаксис cursor.execute("SELECT Name FROM Artist ORDER BY Name LIMIT 3")
    rv = cur.fetchall() # Получаем результат сделанного запроса
    cur.close()
    return (rv[0] if rv else None) if one else rv # выводим одно значение если one = true и весь запрос если false


def change_db(query,args=()):
    cur = get_db().execute(query, args)
    get_db().commit() # Если мы не просто читаем, но и вносим изменения в базу данных - необходимо сохранить транзакцию
    cur.close()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    contact_list = query_db("SELECT * FROM contact")
    return render_template("index.html", contact_list=contact_list)


@app.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == "GET":
        return render_template("create.html", contact=None)

    if request.method == "POST":
        contact = request.form.to_dict()
        values = [contact["name"],contact["surname"],contact["mail"],contact["tel"]]
        change_db("INSERT INTO contact (name,surname,mail,tel) VALUES (?,?,?,?)",values)
        return redirect(url_for("index"))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def udpate(id):

    if request.method == "GET":
        contact = query_db("SELECT * FROM contact WHERE id=?",[id],one=True)
        return render_template("update.html",contact=contact)

    if request.method == "POST":
        contact = request.form.to_dict()
        values = [contact["name"],contact["surname"],contact["mail"],contact["tel"],id]
        change_db("UPDATE contact SET name=?, surname=?, mail=?, tel=? WHERE ID=?",values)
        return redirect(url_for("index"))


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):

    if request.method == "GET":
        contact = query_db("SELECT * FROM contact WHERE id=?",[id],one=True)
        return render_template("delete.html",contact=contact)

    if request.method == "POST":
        change_db("DELETE FROM contact WHERE id = ?",[id])
        return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5004)
