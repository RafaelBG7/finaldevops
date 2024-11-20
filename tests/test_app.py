import json
from app import app

def test_health_check():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 404  # Se não há rota '/', espera-se 404
