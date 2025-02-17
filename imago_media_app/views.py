from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
import time
import unicodedata
from datetime import datetime
from .elasticsearch_service import ElasticsearchService

logger = logging.getLogger(__name__)

def preprocess_query(query):
    """Normalize search query to improve matching."""
    if not query:
        return ""
    query = query.strip().lower()
    query = unicodedata.normalize("NFKD", query)
    return query

def normalize_date(date_str):
    """Converts multiple date formats to a standard format (YYYY-MM-DD)."""
    if not date_str or date_str == "Unknown":
        return "Unknown"
    
    date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    return "Invalid Date"

def normalize_media_item(item):
    """Handles missing fields and normalizes media item data."""
    source = item.get("_source", {})

    return {
        "id": item.get("_id", "N/A"),
        "bildnummer": source.get("bildnummer", "Unknown"),
        "datum": normalize_date(source.get("datum", "Unknown")),
        "suchtext": source.get("suchtext", "").strip(),
        "fotografen": source.get("fotografen", "Unknown"),
        "hoehe": source.get("hoehe", 0),
        "breite": source.get("breite", 0),
        "db": source.get("db", "Unknown")
    }

def remove_duplicates(results):
    """Removes duplicate search results based on 'id'."""
    seen = set()
    unique_results = []
    
    for item in results:
        if item["_id"] not in seen:
            seen.add(item["_id"])
            unique_results.append(item)
    
    return unique_results

class MediaSearchView(APIView):
    def get(self, request):
        query = preprocess_query(request.query_params.get('q', ''))

        if not query:
            logger.warning("Search request missing 'q' parameter")
            return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Received search request with query: {query}")

        es_service = ElasticsearchService()
        start_time = time.time()

        try:
            results = es_service.search_media(query)
            execution_time = time.time() - start_time
            logger.info(f"Search query executed in {execution_time:.2f} seconds")

            if isinstance(results, dict) and "error" in results:
                logger.error(f"Elasticsearch error: {results['error']}")
                return Response({"error": results["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if not results:
                logger.info(f"No results found for query: {query}")
                return Response({"error": "No matching results found"}, status=status.HTTP_404_NOT_FOUND)

            results = remove_duplicates(results)
            formatted_results = [normalize_media_item(item) for item in results]

            logger.info(f"Returning {len(formatted_results)} search results")
            return Response({"results": formatted_results}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Unexpected error during search: {str(e)}", exc_info=True)
            return Response({"error": "Search failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)