def test_hello_world(client):
    response = client.get('/views/hello')
    assert response.text == "Hello, World!"


def test_hello_bob(client):
    response = client.get('/views/hello/bob')
    assert response.text == "Hello, bob!"


# Normal flow
def test_top_viewed_articles_by_month(client):
    response = client.get('/views/article/month/Dawngate/2023/11')
    assert response.json["day"] == 12
