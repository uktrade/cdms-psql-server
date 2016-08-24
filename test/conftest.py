import pytest
import json
from cdms_psql_server.server import app


@pytest.fixture
def test_client():
    client = app.test_client()

    def search_companies(term, limit=50, offset=0):
        resp = client.post(
            '/company-search',
            data=json.dumps({
                'term': term,
                'offset': offset,
                'limit': limit,
            }),
            content_type='application/json',
        )
        return json.loads(resp.data.decode('utf8'))

    client.search_companies = search_companies

    return client
