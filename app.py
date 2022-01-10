from flask import Flask, render_template, request, redirect, flash

import psycopg2

app = Flask(__name__)
app.secret_key = 'some secret'

conn = psycopg2.connect(database="service",
                        user="postgres",
                        password="1234",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')  # запрос к данным формы
            password = request.form.get('password')

            cursor.execute("SELECT login, password FROM service.users")  # выводим список всех логинов
            loginPasswds = list(cursor.fetchall())  # запихиваем все выведенные логины в массив logins вида [("login1",) ...]

            usernamePasswdTulp = (username, password)


            cursor.execute("SELECT full_name FROM service.users WHERE login=%s", (str(username),))
            full_name = list(cursor.fetchall())
            if usernamePasswdTulp in loginPasswds:
                return render_template('account.html', full_name=full_name[0][0])
            else:
                    flash("wrong login or password")
                    return redirect('/login/')
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def reg():


    if request.method == 'POST':

            name = request.form.get('name')
            loginUser = request.form.get('login')
            password = request.form.get('password')

            cursor.execute("SELECT login FROM service.users;", (str(login),))  # выводим все логины из БД

            records = list(cursor.fetchall())  # все логины в формате ("login",) в [("login1"), ("login2"), ("login3"), ...]

            loginUserTulp = (loginUser,)  # создаём кортеж, чтобы проверить, есть ли такой логин в БД

            if loginUserTulp in records:  # для ("login",) в [("login1"), ("login2"), ("login3"), ...]
                flash("User alredy exists")
                return redirect('/registration/')  # переводим пользователя на страницу, где сообщаем ему, что данный логин занят

            else:  # заносим пользователя в БД, если такого логина нет.

                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',(str(name), str(loginUser), str(password),))
                conn.commit()

            return redirect('/login/')

    return render_template('registration.html')


@app.route('/registration/', methods=['POST', 'GET'])
def regErr():
    return render_template('registration.html')
