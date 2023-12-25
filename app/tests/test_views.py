def test_hello_world(client):
    response = client.get('/views/hello')
    assert response.text == "Hello, World!"


def test_hello_bob(client):
    response = client.get('/views/hello/bob')
    assert response.text == "Hello, bob!"


# Normal flow
def test_top_day_for_article_in_month(client):
    response = client.get('/views/top-day/Dawngate/2023/11')
    assert response.json["day"] == 12


def test_views_for_article_in_week(client):
    response = client.get('/views/article/week/Dawngate/2023/1')
    assert response.json["views"] == 129


def test_views_for_article_in_month(client):
    response = client.get('/views/article/month/Dawngate/2023/1')
    assert response.json["views"] == 600


def test_top_articles_for_month(client):
    response = client.get('/views/top-articles/month/2023/1')
    assert False


def test_top_articles_for_week(client):
    response = client.get('/views/top-articles/week/2023/1')
    assert False
