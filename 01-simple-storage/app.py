from collections import namedtuple

from flask import Flask, render_template, redirect,url_for,request, flash

from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
app.secret_key = 'some_secret'

#Message = namedtuple('Message', 'name surname email password')


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
        with open('out.txt','a') as out:
            out.write(name+';'+surname+';'+email+';'+password+'\n')

    else:
        flash('Error: All the form fields are required. ')

    return render_template('index.html', form=form)


@app.route("/viewData", methods=['GET'])
def viewData():
    entities = list()
    with open('out.txt') as f:
        for new_line in f:
            data = new_line.strip().split(';')
            entities.append({'name': data[0], 'surname': data[1], 'email': data[2], 'password': data[3]})
    return render_template('viewData.html',entities=entities)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
