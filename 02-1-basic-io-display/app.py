from flask import Flask, render_template, redirect,url_for,request, flash

from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
app.secret_key = 'some_secret'


class ReusableForm(Form):
    rows = TextField('Name:', validators=[validators.required()])
    columns = TextField('Name:', validators=[validators.required()])


def massiv(line, column):
    newmassiv = list()

    x,y,dx,dy, mas = 0,0,0,1, [[0]*column for i in range(line)]
    for i in range(column*line):
        mas[x][y]=str(i+1)
        if x+dx>=line or x+dx<0 or y+dy>=column or y+dy<0 or mas[x+dx][y+dy]:
            dx,dy = dy,-dx
        x,y = x+dx, y+dy

    for i in range(line):
        newline = ''
        for j in range(column):
            newline = newline + '\t' + str(mas[i][j])
        newmassiv.append(newline)

    return newmassiv

@app.route("/", methods=['GET', 'POST'])
def mainPage():

    form = ReusableForm(request.form)

    if request.method == 'POST':
        rows = request.form['rows'].strip()
        columns = request.form['columns'].strip()

    if form.validate():
        row = int(rows)
        column = int(columns)
        mas = massiv(row, column)
        return render_template('index.html', form=form, mas=mas)

    else:
        flash('Error: All the form fields are required. ')

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
