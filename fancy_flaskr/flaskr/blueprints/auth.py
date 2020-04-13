from flask import Blueprint, url_for, \
        render_template, redirect, flash
from flask_login import current_user, login_user, \
        logout_user, login_required

from ..forms import RegisterForm, LoginForm
from ..models import User
from ..extension import db, login_manager

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        user = User(name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        user = User.query.filter_by(name=name).first()
        login_user(user)
        flash('You have logged in.')
        return redirect(url_for('blog.index'))
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.')
    return redirect(url_for('blog.index'))
