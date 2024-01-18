from flask import flash, render_template, request, redirect, url_for, session, current_app
from flask_login import current_user, login_required

from app import bcrypt
from .forms import ChangePasswordForm, UpdateAccountForm
from app.auth.models import db, User
from app.cookies.views import saved_cookies

from . import account_blueprint

from datetime import datetime, timedelta
import os
import email_validator
import secrets
import json
from PIL import Image

filename = os.path.join(current_app.static_folder, 'data', 'users.json')
with open(filename) as f:
    users_data = json.load(f)

@account_blueprint.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        new_password = form.password.data
        confirm_new_password = form.confirm_password.data
        username = session['username']

        if new_password == confirm_new_password:
            if username in users_data:
                users_data[username] = new_password

                filename = os.path.join(current_app.static_folder, 'data', 'users.json')
                with open(filename, 'w') as f:
                    json.dump(users_data, f)

            flash('Password successfully changed to a new one.', 'success') 
            ## сповіщення, тільки цей рядок
            return redirect(url_for('account_bp.info'))

        flash('Password is not changed.', 'error') 
        ## сповіщення, тільки цей рядок
        return redirect(url_for('account_bp.info'))

    flash('Password is not inserted.', 'info')
    return redirect(url_for('account_bp.info'))

@account_blueprint.route('/info', methods=['GET', 'POST'])
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
        return redirect(url_for('auth_bp.login'))

@account_blueprint.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('account_bp.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    return render_template('account.html', form=form, cp_form=cp_form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@account_blueprint.after_request
def after_request(response):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash("Error related with last_seen", category=("danger"))
    return response