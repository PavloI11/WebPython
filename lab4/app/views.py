from flask import Flask, request, render_template, session, redirect, url_for, flash, make_response
from app import app

from datetime import datetime, timedelta

import json

# Змінні заголовків для кожної сторінки
page_titles = {
    'index': 'Головна сторінка',
    'about': 'Про мене',
    'projects': 'Мої проекти',
    'contact': 'Контакти',
    'login': 'Авторизація',

}

# Список ваших навичок та умінь
my_skills = [
    "Python",
    "Flask",
    "HTML",
    "CSS",
    "JavaScript",
    "SQL",
]

with open('app/users.json') as f:
    users_data = json.load(f)

@app.route('/login', methods=["GET", "POST"])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users_data and users_data[username] == password:
            session['username'] = username
            return redirect(url_for('info'))
        else:
            error_message = 'Невірні дані для входу.'
    return render_template('login.html', error_message=error_message )


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' in session:
        if request.method == 'POST':
            new_password = request.form['new_password']
            username = session['username']

            if username in users_data:
                users_data[username] = new_password

                with open('app/users.json', 'w') as f:
                    json.dump(users_data, f)
                flash('Password successfully changed to a new one.', 'error') ## сповіщення, тільки цей рядок
                return redirect(url_for('info'))

        return render_template('change_password.html')
    else:
        return redirect(url_for('login'))



saved_cookies = {}
@app.route('/info', methods=['GET', 'POST'])
def info():
    username = session.get('username')
    cookies_data = []

    if username:
        if request.method == 'POST':
            if 'cookie_key' in request.form and 'cookie_value' in request.form and 'cookie_expiration' in request.form:
                cookie_key = request.form['cookie_key']
                cookie_value = request.form['cookie_value']
                cookie_expiration = int(request.form['cookie_expiration'])
                expiration_time = datetime.now() + timedelta(seconds=cookie_expiration)
                saved_cookies[cookie_key] = {
                    'value': cookie_value,
                    'expiration': expiration_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

            for key in list(saved_cookies.keys()):
                if f'delete_{key}' in request.form:
                    del saved_cookies[key]

        for key, cookie_data in saved_cookies.items():
            cookies_data.append((key, cookie_data))

        return render_template('info.html', username=username, cookies_data=cookies_data)
    else:
        return redirect(url_for('login'))

@app.route('/add_cookie', methods=['POST'])
def add_cookie():

    cookie_key = request.form['cookie_key']
    cookie_value = request.form['cookie_value']
    cookie_expiration = int(request.form['cookie_expiration'])

    expiration_time = datetime.now() + timedelta(seconds=cookie_expiration)
    saved_cookies[cookie_key] = {
        'value': cookie_value,
        'expiration': expiration_time.strftime('%Y-%m-%d %H:%M:%S'),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return redirect(url_for('info'))


@app.route('/delete_cookie/<key>', methods=['POST'])
def delete_cookie(key):
    if key in saved_cookies:
        del saved_cookies[key]
        flash(f'The cookie with the key "{key}" has been successfully deleted.', 'success')
    return redirect(url_for('info'))

@app.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    saved_cookies.clear()
    flash('All cookies have been successfully deleted.', 'success')
    return redirect(url_for('info'))

@app.route('/logout', methods=['POST'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))





@app.route('/')
def index():
    return render_template('index.html', title=page_titles['index'])

@app.route('/about')
def about():
    return render_template('about.html', title=page_titles['about'])

@app.route('/projects')
def projects():
    return render_template('projects.html', title=page_titles['projects'])

@app.route('/contact')
def contact():
    return render_template('contact.html', title=page_titles['contact'])






if __name__ == '__main__':
    app.run()