import json
from app import app, db, User
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    client = app.test_client()
    yield client
    with app.app_context():
        db.drop_all()

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200

def test_cadastrar_usuario(client):
    response = client.post('/api/cadastrar', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'birthdate': '2000-01-01'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Usuário cadastrado com sucesso!'

def test_cadastrar_usuario_dados_invalidos(client):
    response = client.post('/api/cadastrar', json={
        'username': 'testuser'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'Dados inválidos'

def test_listar_usuarios(client):
    client.post('/api/cadastrar', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'birthdate': '2000-01-01'
    })
    response = client.get('/api/usuarios')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['username'] == 'testuser'
    assert data[0]['email'] == 'testuser@example.com'
    assert data[0]['birthdate'] == '2000-01-01'