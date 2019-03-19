from collections import namedtuple

from flask import Flask, render_template, redirect,url_for,request, flash

from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
app.secret_key = 'some_secret'

Message = namedtuple('Message', 'name surname email password')
tableName = dict.fromkeys(['name','surname','email','password'])


class ReusableForm(Form):
    name = StringField('Name:', validators=[validators.DataRequired()])
    surname = StringField('Surname:', validators=[validators.DataRequired()])
    email = StringField('Email:', validators=[validators.DataRequired(), validators.Length(min=6, max=35)])
    password = StringField('Password:', validators=[validators.DataRequired(), validators.Length(min=3, max=35)])


@app.route("/", methods=['GET', 'POST'])
def mainPage():

    form = ReusableForm(request.form)

    print(form.errors)

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        surname = request.form['surname']

    if form.validate():
        flash('Thanks for registration ' + name)
        tableName['name'] = name
        tableName['surname'] = surname
        tableName['email'] = email
        tableName['password'] = password
        with open('out.txt','a') as out:
            for key,val in tableName.items():
                out.write('{}:{}\n'.format(key,val))

    else:
        flash('Error: All the form fields are required. ')

    return render_template('index.html', form=form)


@app.route("/viewData", methods=['GET'])
def viewData():
    newTable = []
    d = {'name':[],'surname':[],'email':[],'password':[]}
    with open('out.txt') as inp:
        for i in inp.readlines():
            key,val = i.strip().split(':')
            d[key].append(val)
    for k in range(len(d['name'])):
        newTable.append(Message(d['name'][k], d['surname'][k],d['email'][k],d['password'][k]))
    return render_template('viewData.html', newTable=newTable)

if __name__ == '__main__':
    app.run(debug=True)
