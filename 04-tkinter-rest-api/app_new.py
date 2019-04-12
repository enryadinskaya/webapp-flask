import tkinter as tk
from tkinter import ttk, Menu, Listbox, END
from tkinter import messagebox as msg
import sqlite3

contacts = tk.Tk()
contacts.title('Contacts')
contacts.resizable(True, True)


class DB_contact():
    def __init__(self):
        self.contact = sqlite3.connect("data.db")
        self.cursor = self.contact.cursor()
        self.contact.execute("CREATE TABLE IF NOT EXISTS contact (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, surname TEXT NOT NULL, mail TEXT NOT NULL, tel TEXT NOT NULL)")
        self.contact.commit()

    def show_contact(self):
        self.cursor.execute("SELECT * FROM contact")
        rows = self.cursor.fetchall()
        return rows

    def create_contact(self, name, surname, mail, tel):
        self.cursor.execute("INSERT INTO contact (name,surname,mail,tel) VALUES (?,?,?,?)", (name, surname, mail, tel))
        self.contact.commit()

    def search_contact(self, name='', surname='', mail ='', tel =''):
        self.cursor.execute("SELECT * FROM contact WHERE name=? OR surname=? OR mail=? OR tel=?", (name, surname, mail, tel))
        found_rows = self.cursor.fetchall()
        return found_rows

    def update_contact(self, id, name, surname, mail, tel):
        self.cursor.execute("UPDATE contact SET name=?, surname=?, mail=?, tel=? WHERE id=?", (name, surname, mail, tel, id))
        self.contact.commit()

    def delete_contact(self, id):
        self.cursor.execute("DELETE FROM contact WHERE id = ?", [id])
        self.contact.commit()


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


db = DB_contact()


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


def show_command():
    List.delete(0, END)
    for row in db.show_contact():
        List.insert(END, row)


def delete_command():
    db.delete_contact(selected_contact[0])
    show_command()


def update_command():
    db.update_contact(selected_contact[0], name.get(), surname.get(), mail.get(), tel.get())
    show_command()


def add_command():
    db.create_contact(name.get(), surname.get(), mail.get(), tel.get())
    show_command()


def msgBox():
    msg.showinfo('Contacts information','Here you can see all contacts.\nCreate new contact.\nDelete contact.\nUpdate contact')


def _quit():
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
tk.Button(buttons_frame, text='View all', command=show_command, font=('Comic Sans MS', '10', 'normal')).grid(column=0, row=0, sticky=tk.W, padx=8, pady=8)
tk.Button(buttons_frame, text='Add contact', command=add_command, bg='DarkSeaGreen2', font=('Comic Sans MS', '10', 'normal')).grid(column=1, row=0, sticky=tk.W, padx=8, pady=8)
tk.Button(buttons_frame, text='Update contact', command=update_command, font=('Comic Sans MS', '10', 'normal')).grid(column=2, row=0, sticky=tk.W, padx=8, pady=8)
tk.Button(buttons_frame, text='Delete contact', command=delete_command, bg='RosyBrown1', font=('Comic Sans MS', '10', 'normal')).grid(column=3, row=0, sticky=tk.W, padx=8, pady=8)


contacts.mainloop()
