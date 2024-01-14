from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from .models import User

class LoginForm(FlaskForm):
    email = StringField("Ваша електронна пошта", validators=[DataRequired("Це поле обовʼязкове"), Email()])
    password = PasswordField("Ваш пароль", validators=[
                            DataRequired("Це поле обовʼязкове"),
                            Length(min=4, max=10)
                        ])
    remember = BooleanField("Запамʼятати")
    submit = SubmitField("Виконати")

class ChangePasswordForm(FlaskForm):
    password = PasswordField("Новий пароль", validators=[
                            DataRequired("Пароль повинен мати від 4 до 10 символів"),
                            Length(min=4, max=10)
                        ])
    confirm_password = PasswordField("Підтвердити новий пароль", validators=[
                            DataRequired("Пароль повинен мати від 4 до 10 символів"),
                            Length(min=4, max=10)
                        ])
    submit = SubmitField("Виконати")

class CreateTodoForm(FlaskForm):
    task = StringField("Задача", validators=[DataRequired("Це поле обовʼязкове"), Length(min=1, max=100)])
    description = StringField("Опис", validators=[DataRequired("Це поле обовʼязкове"), Length(min=1, max=200)])
    submit = SubmitField("Створити")

class RegisterForm(FlaskForm):
    username = StringField("Ваш Username", validators=[DataRequired(message="Імʼя повинен містити від 4 до 20 символів"), Length(min=4, max=20),
    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', message='Імʼя має містити букви, цифри, крапку та нижнє підкреслення')])

    email = StringField("Ваша електронна пошта", validators=[DataRequired(message="Це поле обовʼязкове"), Email()])

    password = PasswordField("Ваш пароль", validators=[DataRequired(message="Це поле обовʼязкове"), Length(min=6)])

    confirm_password = PasswordField("Підтвердити пароль", validators=[DataRequired(message="Це поле обовʼязкове"), Length(min=6),
    EqualTo('password', message='Паролі не збігаються, спробуйте ще раз')])

    image_file = FileField("Виберіть файл")
    submit = SubmitField("Виконати")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The user with such email has been already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is used already.')