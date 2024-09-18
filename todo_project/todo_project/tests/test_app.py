import pytest
from todo_project import db, app as create_app

@pytest.fixture()
def app():
    app = create_app
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_app_instance(app):
    assert app is not None
    assert app.testing


def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data 


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'About' in response.data


def test_register(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert response.request.path == '/register'


def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert response.request.path == '/login'


def test_register_success(client):
    response = client.post(
        '/register', 
        data={
            'username': 'user',
            'password': 'password',
            'confirm_password': 'password',
        },
        follow_redirects=True
    )
    print(response.data)
    assert response.status_code == 200
    assert response.request.path == '/login'


def test_register_failure(client):
    client.post(
        '/register', 
        data={
            'username': 'user',
            'password': 'password',
            'confirm_password': 'password',
        },
        follow_redirects=True
    )

    response = client.post(
        '/register', 
        data={
            'username': 'user',
            'password': 'other_password',
            'confirm_password': 'other_password',
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == '/register'


def test_login_failure(client):
    response = client.post(
        '/login', 
        data={
            'username': 'user',
            'password': 'password',
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == '/login'


def test_login_success_and_view_tasks(client):
    client.post(
        '/register', 
        data={
            'username': 'user',
            'password': 'password',
            'confirm_password': 'password',
        },
        follow_redirects=True
    )

    response = client.post(
        '/login', 
        data={
            'username': 'user',
            'password': 'password',
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == '/all_tasks'


def test_register_login_create_task(client):
    client.post(
        '/register', 
        data={
            'username': 'user',
            'password': 'password',
            'confirm_password': 'password',
        },
        follow_redirects=True
    )

    client.post(
        '/login', 
        data={
            'username': 'user',
            'password': 'password',
        },
        follow_redirects=True
    )

    response = client.post(
        '/add_task', 
        data={
            'task_name': 'buy_food',
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Task Created" in response.data