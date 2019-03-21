from flask import Flask, render_template, redirect,url_for,request, flash

from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
app.secret_key = 'some_secret'


class ReusableForm(Form):
    numbers = TextField('Name:', validators=[validators.required()])


def massiv(numbers):
    newmassiv = list()
    line = int(numbers[0])
    column = int(numbers[1])
    mas = [[0]*column for i in range(line)]

    i, j = 0, 0
    for k in range(1, ((line*column)+1)):
        mas[i][j] = k
        if k == line*column:
            break

        if line < column:
            if i <= j+1 and i+j < column-1:
                j += 1
            elif i < j-1 and i+j >= column-1:
                i += 1
            elif i >= j-1 and i+j >= column-1:
                j -= 1
            elif i > j+1 and i+j < column-1:
                i -= 1

        elif line == column:
            if i <= j+1 and i+j < column-1:
                j += 1
            elif i < j and i+j >= column-1:
                i += 1
            elif i >= j and i+j > column-1:
                j -= 1
            elif i > j+1 and i+j <= column-1:
                i -= 1

        elif line > column:
            if i <= j+1 and i+j < column-1:
                j += 1
            elif i < j+1 and i+j >= column-1:
                i += 1
            elif i >= j+1 and i+j > column:
                j -= 1
            elif i > j+1 and i+j <= column:
                i -= 1
    for i in range(line):
        newline = ''
        for j in range(column):
            newline = newline + ' ' + str(mas[i][j])
        newmassiv.append(newline)

    return newmassiv

@app.route("/", methods=['GET', 'POST'])
def mainPage():

    form = ReusableForm(request.form)

    if request.method == 'POST':
        numbers = request.form['numbers'].strip().split()

    if form.validate():
        mas = massiv(numbers)
        return render_template('index.html', form=form, mas=mas)

    else:
        flash('Error: All the form fields are required. ')

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
