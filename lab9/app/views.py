import os
import secrets
from flask import request, render_template, session, redirect, url_for, flash
from app import app
from .forms import LoginForm, ChangePasswordForm, CreateTodoForm, RegisterForm, UpdateAccountForm
from .models import db, Todo, User

from datetime import datetime, timedelta
from flask_login import login_user, current_user, logout_user, login_required

import json
import email_validator

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

filename = os.path.join(app.static_folder, 'data', 'users.json')
with open(filename) as f:
    users_data = json.load(f)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('info'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        image_file = form.image_file.data
        if password == confirm_password:
            new_user = User(username=username, email=email, password=password, image_file=image_file)
            db.session.add(new_user)
            db.session.commit()
        flash("Аккаунт зареєстровано", category=("success"))
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('info'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        form_email = form.email.data
        form_password = form.password.data
        form_remember = form.remember.data

        if user and user.validate_password(form_password) and user.email == form_email:
            if form_remember:
                session['username'] = user.username
                flash("Login is successful", category=("success"))
                login_user(user, remember=form.remember.data)
                return redirect(url_for('account'))
            else:
                flash("You didn't remember yourself", category=("info"))
        else:
            flash("Login is failed", category=("warning"))

    return render_template('login.html', form=form)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        new_password = form.password.data
        confirm_new_password = form.confirm_password.data
        username = session['username']

        if new_password == confirm_new_password:
            if username in users_data:
                users_data[username] = new_password

                filename = os.path.join(app.static_folder, 'data', 'users.json')
                with open(filename, 'w') as f:
                    json.dump(users_data, f)

            flash('Password successfully changed to a new one.', 'success') 
            ## сповіщення, тільки цей рядок
            return redirect(url_for('info'))

        flash('Password is not changed.', 'error') 
        ## сповіщення, тільки цей рядок
        return redirect(url_for('info'))

    flash('Password is not inserted.', 'info')
    return redirect(url_for('info'))

saved_cookies = {}

@app.route('/users')
@login_required
def users():
    all_users = User.query.all()
    return render_template('users.html', all_users=all_users)

@app.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    username = session.get('username')
    form = ChangePasswordForm()
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

        return render_template('info.html', form=form, username=username, cookies_data=cookies_data)
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
    logout_user()
    return redirect(url_for('login'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    cp_form = ChangePasswordForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)

        db.session.commit()
        flash("Account is updated", category=("success"))
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    return render_template('account.html', form=form, cp_form=cp_form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.after_request
def after_request(response):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash("Error related with last_seen", category=("danger"))
    return response

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

@app.route("/todo")
@login_required
def todo():
    form = CreateTodoForm()
    list = db.session.query(Todo).all()

    return render_template('todo.html', form=form, list=list)

@app.route("/create_todo", methods=['POST'])
def create_todo():
    form = CreateTodoForm()

    if form.validate_on_submit():
        task = form.task.data
        description = form.description.data
        todo = Todo(title=task, description=description, complete=False)
        db.session.add(todo)
        db.session.commit()
        flash("Створення виконано", category=("success"))
        return redirect(url_for("todo"))

    flash("Помилка при створенні", category=("danger"))
    return redirect(url_for("todo"))

@app.route("/read_todo/<int:todo_id>")
def read_todo(todo_id=None):
    todo = Todo.query.get_or_404(todo_id)
    return redirect(url_for("todo"))

@app.route("/update_todo/<int:todo_id>")
def update_todo(todo_id=None):
    todo = Todo.query.get_or_404(todo_id)

    todo.complete = not todo.complete
    db.session.commit()
    flash("Оновлення виконано", category=("success"))
    return redirect(url_for("todo"))

@app.route("/delete_todo/<int:todo_id>")
def delete_todo(todo_id=None):
    todo = Todo.query.get_or_404(todo_id)

    db.session.delete(todo)
    db.session.commit()
    flash("Видалення виконано", category=("success"))
    return redirect(url_for("todo"))
