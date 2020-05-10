from flask import Blueprint, url_for, \
        render_template, redirect, flash, abort
from flask_login import current_user, login_user, \
        logout_user, login_required

from ..models import Post
from ..extension import db
from ..forms import PostForm

blog_bp = Blueprint('blog', __name__, url_prefix='/post')


@blog_bp.route('/')
def index():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('blog/index.html', posts=posts)


@blog_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        author_id = current_user.id
        post = Post(title=title, body=body, author_id=author_id)
        db.session.add(post)
        db.session.commit()
        flash('Create post successfully!')
        return redirect(url_for('blog.index'))
    return render_template('blog/create.html', form=form)


@blog_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get_or_404(id)
    if current_user.id != post.author_id:
        abort(404)
    form = PostForm(title=post.title, body=post.body)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('Your post has updated!')
        return redirect(url_for('blog.index'))
    return render_template('blog/update.html', form=form, post=post)


@blog_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if current_user.id != post.author_id:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!')
    return redirect(url_for('blog.index'))
