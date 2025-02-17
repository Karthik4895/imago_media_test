import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from elasticsearch_service import ElasticsearchService  # Import your search service

@pytest.fixture
def es_service():
    return ElasticsearchService()

def test_es_search_valid_query(es_service):
    results = es_service.search_media("test")
    assert isinstance(results, list)
    assert all("suchtext" in item["_source"] for item in results)

def test_es_search_invalid_query(es_service):
    results = es_service.search_media("")
    assert results == []  # Expecting empty results for empty query


@pytest.mark.django_db
def test_media_search_success():
    client = APIClient()
    response = client.get(reverse("media_search") + "?q=test")
    
    assert response.status_code == 200
    assert "results" in response.data
    assert isinstance(response.data["results"], list)

@pytest.mark.django_db
def test_media_search_no_query():
    client = APIClient()
    response = client.get(reverse("media_search"))
    
    assert response.status_code == 400
    assert response.data["error"] == "Query parameter 'q' is required"

@pytest.mark.django_db
def test_media_search_no_results():
    client = APIClient()
    response = client.get(reverse("media_search") + "?q=nonexistentdata")
    
    assert response.status_code == 404
    assert response.data["error"] == "No matching results found"
