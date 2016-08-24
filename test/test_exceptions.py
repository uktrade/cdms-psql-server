import json


def test_empty_post_gives_400(test_client):
    resp = test_client.post(
        '/company-search',
        data=json.dumps({}),
        content_type='application/json',
    )
    assert resp.status_code == 400
