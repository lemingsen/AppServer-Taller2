"""Root endpoints tests"""


def test_ping(client):
    response = client.get('/ping')
    assert response.get_json() == {"ping": 1}