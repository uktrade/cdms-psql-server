import os

import psycopg2
from flask import request, jsonify
from werkzeug.exceptions import BadRequest

from .json_exceptions import make_json_app


app = make_json_app(__name__)

app.config['DATABASE_URI'] = os.environ['DATABASE_URI']

SEARCH_COMPANIES_SQL = '''
SELECT company_id, company_name
FROM (
    SELECT
        "AccountSet"."Name" as company_name,
        "AccountSet"."AccountId" as company_id,
        to_tsvector("AccountSet"."Name") as name,
        to_tsvector("AccountSet"."optevia_PostCode") as postcode,
        to_tsvector("AccountSet"."PrimaryContactId_Name") as contact_name,
        to_tsvector(coalesce(string_agg("detica_interactionSet"."Subject", ' '))) as interaction_subjects
    FROM "AccountSet"
    LEFT OUTER JOIN "detica_interactionSet" ON
        "AccountSet"."AccountId" = "detica_interactionSet"."optevia_Organisation_Id"
    GROUP BY company_name, company_id
) searchable
    WHERE searchable.postcode @@ to_tsquery(%s)
    OR searchable.name @@ to_tsquery(%s)
    OR searchable.contact_name @@ to_tsquery(%s)
    OR searchable.interaction_subjects @@ to_tsquery(%s)
    OFFSET %s
    LIMIT %s
;
'''
conn = psycopg2.connect(app.config['DATABASE_URI'])


@app.route("/company-search", methods=['POST'])
def search_companies():
    try:
        term = ' & '.join(request.json['term'].split(' '))
        limit = request.json.get('limit', 50)
        offset = request.json.get('offset', 0)
    except KeyError:
        raise BadRequest('Pass `term` key in request JSON.')
    cur = conn.cursor()
    cur.execute(
        SEARCH_COMPANIES_SQL,
        (term, term, term, term, offset, limit),
    )
    result_dicts = [
        {'id': company_id, 'name': company_name}
        for company_id, company_name in cur.fetchall()
    ]
    return jsonify(companies=result_dicts)


if __name__ == "__main__":
    app.run()
