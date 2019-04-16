import tkinter as tk
from tkinter import ttk, Menu, END
from tkinter import messagebox as msg

from flask import Flask
from flask_restful import reqparse, Api, Resource
import requests
import sqlite3
import threading


contacts = tk.Tk()
app = Flask(__name__)
main_url = "http://localhost:5000/contacts"

def flask_main():
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

    app.run()


def tk_main():
    contacts.title('Contacts')
    contacts.resizable(True, True)


    class ToolTip(object):
        def __init__(self, widget):
            self.widget = widget
            self.tip_window = None

        def show_tip(self, tip_text):
            if self.tip_window or not tip_text:
                return
            x, y, _cx, cy = self.widget.bbox('insert')
            x = x + self.widget.winfo_rootx() - 15
            y = y + cy + self.widget.winfo_rooty() + 15
            self.tip_window = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry('+%d+%d' % (x, y))

            label = tk.Label(tw, text=tip_text, justify=tk.LEFT, background='#ffffe0', relief=tk.SOLID, borderwidth=1,
                             font=('Arial', '8', 'normal'))
            label.pack(ipadx=1)

        def hide_tip(self):
            tw = self.tip_window
            self.tip_window = None
            if tw:
                tw.destroy()


    def create_ToolTip(widget, text):
        toolTip = ToolTip(widget)
        def enter(event):
            toolTip.show_tip(text)
        def leave(event):
            toolTip.hide_tip()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)


    def get_selected_row(event):
        global selected_contact
        index = List.curselection()[0]
        selected_contact = List.get(index)
        name_entered.delete(0, END)
        name_entered.insert(END, selected_contact[1])
        surname_entered.delete(0, END)
        surname_entered.insert(END, selected_contact[2])
        mail_entered.delete(0, END)
        mail_entered.insert(END, selected_contact[3])
        tel_entered.delete(0, END)
        tel_entered.insert(END, selected_contact[4])


    def command(command=None):
        global main_url
        if command == 'delete':
            requests.delete(main_url + '/' + str(selected_contact[0]))
        elif command == 'add':
            requests.post(main_url, data={'name': name.get(), 'surname': surname.get(), 'mail': mail.get(), 'tel': tel.get()})
        elif command == 'update':
            requests.put(main_url + '/' + str(selected_contact[0]), data={'name': name.get(), 'surname': surname.get(), 'mail': mail.get(), 'tel': tel.get()})
        List.delete(0, END)
        req_ob = requests.get(main_url)
        result = req_ob.json()
        for row in result:
            List.insert(END, row)


    def msgBox():
        msg.showinfo('Contacts information','Here you can see all contacts.\nCreate new contact.\nDelete contact.\nUpdate contact')


    def _quit():
        answer = msg.askyesno('Python Message', 'Do you really want to exit?')
        if answer == 1:
            contacts.quit()


    menu_bar = Menu(contacts)
    contacts.config(menu=menu_bar)
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label='Exit', command=_quit)
    menu_bar.add_cascade(label='File', menu=file_menu)

    help_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label='About', command=msgBox)


    mighty = tk.LabelFrame(contacts, text='Contact information')
    mighty.grid(column=0, row=0, padx=8, pady=8)
    mighty.configure(background='ivory')

    a_lable = ttk.Label(mighty, text='Name:')
    a_lable.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
    a_lable.configure(background='ivory', font=('Comic Sans MS', '12', 'normal'))
    name = tk.StringVar()
    name_entered = ttk.Entry(mighty, width=30, textvariable=name)
    name_entered.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
    name_entered.focus()
    create_ToolTip(name_entered,'Contact name')


    a_lable = ttk.Label(mighty, text='Surname:')
    a_lable.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
    a_lable.configure(background='ivory', font=('Comic Sans MS', '12', 'normal'))
    surname = tk.StringVar()
    surname_entered = ttk.Entry(mighty, width=30, textvariable=surname)
    surname_entered.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
    surname_entered.focus()
    create_ToolTip(surname_entered,'Contact surname')

    a_lable = ttk.Label(mighty, text='Mail:')
    a_lable.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
    a_lable.configure(background='ivory', font=('Comic Sans MS', '12', 'normal'))
    mail = tk.StringVar()
    mail_entered = ttk.Entry(mighty, width=30, textvariable=mail)
    mail_entered.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
    mail_entered.focus()
    create_ToolTip(mail_entered,'Contact mail')

    a_lable = ttk.Label(mighty, text='Telephone:')
    a_lable.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)
    a_lable.configure(background='ivory', font=('Comic Sans MS', '12', 'normal'))
    tel = tk.StringVar()
    tel_entered = ttk.Entry(mighty, width=30, textvariable=tel)
    tel_entered.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)
    tel_entered.focus()
    create_ToolTip(tel_entered,'Contact telephone')


    list_frame = ttk.LabelFrame(mighty)
    list_frame.grid(column=0, row=4, padx=8, pady=8, columnspan=2)
    List = tk.Listbox(list_frame, height=20, width=70)
    List.grid(row=8, column=0, columnspan=2)


    scr = tk.Scrollbar(list_frame)
    scr.grid(row=8, column=2, rowspan=12)
    List.configure(yscrollcommand=scr.set)
    scr.configure(command=List.yview)
    List.bind('<<ListboxSelect>>', get_selected_row)


    buttons_frame = tk.Frame(mighty)
    buttons_frame.grid(column=0, row=15, columnspan=2, sticky=tk.W)
    buttons_frame.configure(background='ivory')
    tk.Button(buttons_frame, text='View all', command=command, font=('Comic Sans MS', '10', 'normal')).grid(column=0, row=0, sticky=tk.W, padx=8, pady=8)
    tk.Button(buttons_frame, text='Add contact', command=lambda: command('add'), bg='DarkSeaGreen2', font=('Comic Sans MS', '10', 'normal')).grid(column=1, row=0, sticky=tk.W, padx=8, pady=8)
    tk.Button(buttons_frame, text='Update contact', command=lambda: command('update'), font=('Comic Sans MS', '10', 'normal')).grid(column=2, row=0, sticky=tk.W, padx=8, pady=8)
    tk.Button(buttons_frame, text='Delete contact', command=lambda: command('delete'), bg='RosyBrown1', font=('Comic Sans MS', '10', 'normal')).grid(column=3, row=0, sticky=tk.W, padx=8, pady=8)


    contacts.mainloop()


if __name__ == "__main__":
    flt = threading.Thread(target=flask_main)
    flt.daemon = True
    flt.start()
    tk_main()
