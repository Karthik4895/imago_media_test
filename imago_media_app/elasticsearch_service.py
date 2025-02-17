import logging
from elasticsearch import exceptions
from .es_client import es_client

logger = logging.getLogger(__name__)

class ElasticsearchService:
    def search_media(self, query, page=1, page_size=10):
        body = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"suchtext": query}},
                        {"match": {"fotografen": query}}
                    ]
                }
            },
            "from": (page - 1) * page_size,
            "size": page_size
        }

        try:
            response = es_client.search(index="imago", body=body)
            return response.get('hits', {}).get('hits', [])
        except exceptions.ConnectionError as e:
            logger.error(f"Elasticsearch Connection Error: {str(e)}")
            return {"error": "Failed to connect to Elasticsearch"}
        except exceptions.ElasticsearchException as e:
            logger.error(f"Elasticsearch Query Error: {str(e)}")
            return {"error": "Elasticsearch query failed"}