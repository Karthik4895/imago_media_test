from elasticsearch import Elasticsearch
from django.conf import settings

es_client = Elasticsearch(settings.ELASTICSEARCH_CONFIG["hosts"], verify_certs=False)
