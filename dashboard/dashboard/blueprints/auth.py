from flask import Blueprint, redirect, url_for, render_template, flash

from ..forms import RegisterForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('Register successfully! Please login to continue.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return 'login page'


@auth_bp.route('/logout')
def logout():
    return 'logout page'
