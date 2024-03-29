def test_search_one(test_client):
    resp = test_client.search_companies('icandy')
    assert len(resp['companies']) == 1
    assert resp['companies'][0]['name'] == 'iCandy UK'

def test_search_interaction_subject(test_client):
    resp = test_client.search_companies('stand number at Milipol in Qatar')
    assert resp['companies'][0]['name'] == 'Crewshield Limited'
