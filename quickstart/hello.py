from flask import (Flask, request, redirect, url_for,
        render_template, abort)
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('hello'))
    return 'You are going to login in this page.'


@app.route('/user/<username>')
def profile(username):
    return 'User %s\'s profile' % escape(username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return 'Subpath %s' % escape(subpath)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/404')
def error_404():
    abort(404)
