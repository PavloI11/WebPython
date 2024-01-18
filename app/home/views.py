from flask import render_template

from . import home_blueprint

# Список ваших навичок та умінь
my_skills = [
    "Python",
    "Flask",
    "HTML",
    "CSS",
    "JavaScript",
    "SQL",
]


# Змінні заголовків для кожної сторінки
page_titles = {
    'index': 'Головна сторінка',
    'about': 'Про мене',
    'projects': 'Мої проекти',
    'contact': 'Контакти',
    'login': 'Авторизація',
}

@home_blueprint.route('/')
def index():
    return render_template('index.html', title=page_titles['index'])

@home_blueprint.route('/about')
def about():
    return render_template('about.html', title=page_titles['about'])

@home_blueprint.route('/projects')
def projects():
    return render_template('projects.html', title=page_titles['projects'])

@home_blueprint.route('/contact')
def contact():
    return render_template('contact.html', title=page_titles['contact'])