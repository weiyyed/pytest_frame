# -*- coding: utf-8 -*-

from flask import Flask, request, session, redirect, url_for, jsonify

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

users = [
    {'name': 'Lucy', 'age': 18, 'favor': 'Music'},
    {'name': 'Kate', 'age': 16, 'favor': 'Game'},
    {'name': 'John', 'age': 20, 'favor': 'Math'},
]


@app.route('/')
def index():
    return 'Hello world'


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return 'login page'
    elif request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            if username == 'admin' and password == 'changeme':
                session['user'] = username
                return make_json_resp(data=username, link='/')
            else:
                return make_json_resp(status=-101, msg='unmatched username and password', link='/login')
        except KeyError:
            return make_json_resp(status=-102, msg='invalid parameters', link='/login')


@app.route('/users/', methods=['GET', 'POST'])
def user_page():
    if request.method == 'GET':
        return make_json_resp(data=users, link='/users')
    elif request.method == 'POST':
        try:
            name = request.form['name']
            age = request.form['age']
            favor = request.form['favor']

            user = dict(name=name, age=age, favor=favor)
            users.append(user)
            return make_json_resp(data=user, msg='Add user {} successfully'.format(name), link='/users')
        except KeyError:
            return make_json_resp(status=-201, msg='invalid parameters')
    elif request.method == 'DELETE':
        try:
            name = request.form['name']

            count = 0
            for user in users:
                if name == user.get('name'):
                    count += 1
                    users.remove(user)
            return make_json_resp(msg='delete {} user(s)'.format(count), link='/users')
        except KeyError:
            return make_json_resp(status=-202, msg='invalid parameters')


@app.before_request
def login_check():
    if request.path == '/login/':
        return

    if session.get('user') is None:
        return redirect(url_for('login'))


def make_json_resp(**kwargs):
    result = {}
    result['status'] = kwargs.get('status', 0)
    result['msg'] = kwargs.get('msg', 'ok')
    result['data'] = kwargs.get('data')
    result['link'] = kwargs.get('link')

    return jsonify(result)


if __name__ == '__main__':
    app.run()