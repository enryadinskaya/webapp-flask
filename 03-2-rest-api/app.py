from flask import Flask
from flask import request, jsonify, render_template, redirect, url_for, g
import sqlite3


app = Flask(__name__)
DATABASE = "data.db"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/contact/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM contact;').fetchall()

    return jsonify(all_books)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/contact', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    name = query_parameters.get('name')
    surname = query_parameters.get('surname')
    mail = query_parameters.get('mail')
    tel = query_parameters.get('tel')

    query = "SELECT * FROM contact WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if name:
        query += ' name=? AND'
        to_filter.append(name)
    if surname:
        query += ' surname=? AND'
        to_filter.append(surname)
    if mail:
        query += ' mail=? AND'
        to_filter.append(mail)
    if tel:
        query += ' tel=? AND'
        to_filter.append(tel)
    if not (id or name or surname or tel or mail):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
