from datetime import datetime

def test_status(client):
    response = client.get('/api/v1/status')

    assert response.status_code == 200

    data = response.json()
    
    assert datetime.fromisoformat(data['updated_at'])

    db_data = data['dependencies']['database'] 
    assert db_data['version'] == '16.13 (Debian 16.13-1.pgdg12+1)'
    assert db_data['max_connections'] == 100
    assert db_data['opened_connections'] == 1
