from flask import Flask
from flask import request, jsonify, render_template, redirect, url_for, g
from flask_restful import reqparse, abort, Api, Resource
import sqlite3


app = Flask(__name__)
DATABASE = "data.db"
api = Api(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    return db


def abort_if_todo_doesnt_exist(contact_id):
    if contact_id not in tab_contacts:
        abort(404, message="Contact {} doesn't exist".format(contact_id))


def change_db(query,args=()):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur_db = conn.execute(query,args)
    conn.commit() # Если мы не просто читаем, но и вносим изменения в базу данных - необходимо сохранить транзакцию
    cur_db.close()

def update_contact():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_contacts = cur.execute('SELECT * FROM contact;').fetchall()
    tab_contacts = {}
    for element in all_contacts:
        num_contact = 'id%i' % element['id']
        tab_contacts[num_contact] = element
    return tab_contacts


tab_contacts = update_contact()

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('surname')
parser.add_argument('tel')
parser.add_argument('mail')


class Todo(Resource):
    def get(self, contact_id):
        num_id = 'id' + contact_id
        abort_if_todo_doesnt_exist(num_id)
        return tab_contacts[num_id]

    def delete(self, contact_id):
        num_id = 'id' + contact_id
        abort_if_todo_doesnt_exist(num_id)
        change_db("DELETE FROM contact WHERE id = ?",[int(contact_id)])
        tab_contacts = update_contact()
        return tab_contacts

    def put(self, contact_id):
        num_id = 'id' + contact_id
        args = parser.parse_args()
        global tab_contacts
        if args['name'] == None:
            args['name'] = tab_contacts[num_id]['name']
        if args['surname'] == None:
            args['surname'] = tab_contacts[num_id]['surname']
        if args['mail'] == None:
            args['mail'] = tab_contacts[num_id]['mail']
        if args['tel'] == None:
            args['tel'] = tab_contacts[num_id]['tel']

        values = [args['name'], args['surname'], args['mail'], args['tel'], int(contact_id)]
        change_db("UPDATE contact SET name=?, surname=?, mail=?, tel=? WHERE ID=?",values)
        tab_contacts = update_contact()
        return tab_contacts[num_id]


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return tab_contacts

    def post(self):
        args = parser.parse_args()
        values = [args['name'], args['surname'], args['mail'], args['tel']]
        change_db("INSERT INTO contact (name,surname,mail,tel) VALUES (?,?,?,?)",values)
        tab_contacts = update_contact()
        return tab_contacts

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/contacts')
api.add_resource(Todo, '/contacts/<contact_id>')


if __name__ == '__main__':
    app.run(debug=True)
