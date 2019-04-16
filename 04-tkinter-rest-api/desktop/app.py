import tkinter as tk
from tkinter import ttk, Menu, END
from tkinter import messagebox as msg
import requests

contacts = tk.Tk()
contacts.title('Contacts')
contacts.resizable(True, True)

#main_url = "http://localhost:5000/contacts"


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
    if command == 'delete':
        requests.delete(main_url.get() + '/' + str(selected_contact[0]))
    elif command == 'add':
        requests.post(main_url.get(), data={'name': name.get(), 'surname': surname.get(), 'mail': mail.get(), 'tel': tel.get()})
    elif command == 'update':
        requests.put(main_url.get() + '/' + str(selected_contact[0]), data={'name': name.get(), 'surname': surname.get(), 'mail': mail.get(), 'tel': tel.get()})
    List.delete(0, END)
    req_ob = requests.get(main_url.get())
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

a_lable = ttk.Label(contacts, text='Url:')
a_lable.grid(column=0, row=0, sticky=tk.E, padx=3, pady=3)
main_url = tk.StringVar()
main_url_entered = ttk.Entry(contacts, width=70, textvariable=main_url)
main_url_entered.grid(column=1, row=0, sticky=tk.W, padx=3, pady=3)

mighty = tk.LabelFrame(contacts, text='Contact information')
mighty.grid(row=1, padx=8, pady=8, columnspan=2)
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
