from flask import Flask
from flask_restful import reqparse, Api, Resource
import sqlite3


app = Flask(__name__)
DATABASE = "data.db"
api = Api(app)


def change_db(query,args=()):
    conn = sqlite3.connect(DATABASE)
    cur_db = conn.execute(query, args)
    conn.commit()
    cur_db.close()


def update_contact():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    all_contacts = cur.execute('SELECT * FROM contact;').fetchall()
    return all_contacts


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('surname')
parser.add_argument('tel')
parser.add_argument('mail')


class Contact(Resource):

    def delete(self, contact_id):
        change_db("DELETE FROM contact WHERE id = ?",[int(contact_id)])


    def put(self, contact_id):
        args = parser.parse_args()
        values = [args['name'], args['surname'], args['mail'], args['tel'], int(contact_id)]
        change_db("UPDATE contact SET name=?, surname=?, mail=?, tel=? WHERE ID=?",values)


class ContactList(Resource):
    def get(self):
        return update_contact()

    def post(self):
        args = parser.parse_args()
        values = [args['name'], args['surname'], args['mail'], args['tel']]
        change_db("INSERT INTO contact (name,surname,mail,tel) VALUES (?,?,?,?)", values)


api.add_resource(ContactList, '/contacts')
api.add_resource(Contact, '/contacts/<contact_id>')

if __name__ == '__main__':
    app.run(debug=True)
