# Media Retrieval System

## Overview
This project is a Django-based media retrieval system that integrates with Elasticsearch to perform keyword-based searches on media records. The system ensures efficient search, data normalization, scalability, and maintainability while handling large datasets.

## Technologies Used
- **Django** - Backend framework for API development
- **Django REST Framework** - API implementation
- **Elasticsearch** - Full-text search and analytics engine
- **Python Logging** - Monitoring and debugging

## Features
### 1. Search and Retrieval
- Retrieves media records from the Elasticsearch index (`imago`).
- Performs keyword-based search on fields like `suchtext`, `fotografen`, etc.
- Uses `from` and `size` for pagination (to be replaced with `search_after` for better performance on large datasets).

### 2. Data Normalization
- Handles missing fields gracefully by returning 'N/A' when a field is absent.
- Proposed: Implement data transformations and enrichment techniques to improve searchability.

### 3. Problem Identification & Solution Proposal
- **Issue**: Using `from` and `size` for pagination is inefficient for large datasets.
- **Impact**: Query performance degrades significantly with deep pagination.
- **Solution**: Replace with `search_after` for efficient deep pagination and use Celery to offload heavy queries.

### 4. Scalability & Maintainability
- Current setup can handle moderate data volumes but needs improvement.
- **Proposed:**
  - Use `search_after` instead of `from` and `size` for better performance.
  - Integrate Celery for asynchronous processing of large queries.
  - Implement caching strategies to reduce redundant queries.

### 5. Monitoring & Testing
- Implemented logging for capturing Elasticsearch queries and errors.
- Proposed:
  - Add unit tests for API endpoints.
  - Write integration tests to verify Elasticsearch interactions.
  - Implement load testing to measure scalability.

## Setup Instructions
1. Clone the repository:
   ```sh
   git clone <repo_url>
   cd <project_folder>
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure environment variables in `.env` (Example):
   ```env
   ELASTICSEARCH_HOST=https://5.75.227.63
   ELASTICSEARCH_PORT=9200
   ELASTICSEARCH_INDEX=imago
   ELASTICSEARCH_USER=elastic
   ELASTICSEARCH_PASSWORD=rQQtbktwzFqAJS1h8YjP
   ```
4. Run Django server:
   ```sh
   python manage.py runserver
   ```
5. Test API endpoint:
   ```sh
   curl -X GET "http://127.0.0.1:8000/api/search?q=keyword"
   ```

## Future Enhancements
- Implement `search_after` for better pagination.
- Introduce Celery for handling large data processing tasks.
- Improve indexing strategy to optimize Elasticsearch queries.
- Implement authentication and rate limiting for security.

