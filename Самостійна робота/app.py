from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedbacks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secretkey' 
db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=False)

class FeedbackForm(FlaskForm):
    name = StringField('Імя', validators=[DataRequired()])
    comment = TextAreaField('Відгук', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FeedbackForm()
    if form.validate_on_submit():
        name = form.name.data
        comment = form.comment.data
        feedback = Feedback(name=name, comment=comment)
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('index'))
    
    feedbacks = Feedback.query.all()
    return render_template('index.html', form=form, feedbacks=feedbacks)

@app.route('/clear_database')
def clear_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
