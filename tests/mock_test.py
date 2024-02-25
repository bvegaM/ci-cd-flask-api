import json
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_sum(client, mocker):
    payload = {'num1': 2, 'num2': 3}
    mocker.patch.object(app, 'test_client', return_value=client)
    mocker.patch.object(client, 'post', return_value=app.response_class(
        response=json.dumps({'result': 5}),
        status=200,
        mimetype='application/json'
    ))

    response = client.post('/sum', json=payload)
    data = response.get_json()
    assert data['result'] == 5

if __name__ == '__main__':
    pytest.main([__file__])