from flaskr.models import User, Post

from .conftest import fakes, AuthActions


def test_create_post(auth_app):
    client = auth_app.test_client()
    auth = AuthActions(client)
    res = client.get('/post/create')
    assert res.status_code == 302
    assert '/auth/login' in res.headers['Location']
    user = fakes['users'][0]
    auth.login(user['username'], user['password'])
    res = client.get('/post/create')
    assert res.status_code == 200
    res = client.post('/post/create', data={
        'title': 'test create post',
        'body': 'None'})
    assert res.status_code == 302
    with auth_app.app_context():
        posts = Post.query.all()
        assert len(posts) == 3


def test_update_post(auth_app):
    client = auth_app.test_client()
    auth = AuthActions(client)
    res = client.get('/post/1/update')
    assert res.status_code == 302
    assert '/auth/login' in res.headers['Location']
    user = fakes['users'][0]
    auth.login(user['username'], user['password'])
    with auth_app.app_context():
        user_ins = User.query.filter_by(name=user['username']).first()
        user_id = user_ins.id
        posts = Post.query.filter_by(author_id=user_id).all()
    for post in posts:
        url = '/post/%d/update' % post.id
        res = client.get(url)
        assert res.status_code == 200
        res = client.post(url, data={
            'title': 'test update post',
            'body': 'None'})
        assert res.status_code == 302
    with auth_app.app_context():
        user_ins = User.query.filter_by(name=user['username']).first()
        user_id = user_ins.id
        posts = Post.query.filter_by(author_id=user_id).all()
    for post in posts:
        assert post.title == 'test update post'
        assert post.body == 'None'


def test_delete_post(auth_app):
    client = auth_app.test_client()
    auth = AuthActions(client)
    res = client.get('/post/1/delete')
    assert res.status_code == 405
    res = client.post('/post/1/delete')
    assert res.status_code == 302
    assert '/auth/login' in res.headers['Location']
    user = fakes['users'][0]
    auth.login(user['username'], user['password'])
    client.post('/post/1/delete')
    with auth_app.app_context():
        target = Post.query.get(1)
        assert target is None
