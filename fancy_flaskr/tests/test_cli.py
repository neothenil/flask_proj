from flaskr.extension import db
from flaskr.models import User, Post


def test_create_db(app, runner):
    result = runner.invoke(args=['create-db'])
    assert 'database created' in result.output
    with app.app_context():
        user = User(name='testing')
        user.set_password('testing')
        post = Post(title='testing', body='testing')
        post.author = user
        db.session.add_all([user, post])
        db.session.commit()
        users = User.query.all()
        posts = Post.query.all()
        assert len(users) == 1
        assert len(posts) == 1
    result = runner.invoke(args=['create-db', '--force'])
    assert 'old database dropped' in result.output
    with app.app_context():
        users = User.query.all()
        posts = Post.query.all()
        assert len(users) == 0
        assert len(posts) == 0


def test_forge(app, runner):
    result = runner.invoke(args=
            ['forge', '--user-num', '2', '--post-num', '10'])
    assert 'Done' in result.output
    with app.app_context():
        users = User.query.all()
        posts = Post.query.all()
        assert len(users) == 2
        assert len(posts) == 10
