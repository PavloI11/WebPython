from flask import Flask, render_template

app = Flask(__name__)

# Змінні заголовків для кожної сторінки
page_titles = {
    'index': 'Головна сторінка',
    'about': 'Про мене',
    'projects': 'Мої проекти',
    'contact': 'Контакти',
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
