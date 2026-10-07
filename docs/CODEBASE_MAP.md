# Codebase Map

## Directory Layout & Django Apps
- `polyforge/`: Main Django project configuration (settings, urls).
- `migration/`: The core Django app handling Polygon integration.
- `migration/storage/`: Abstraction layer for cloud storage (S3, Azure, Local).

## Models and Relationships
- `Problem`: Stores `polygon_id`, `name`, `difficulty`, `tags`.
- `TestCase`: Belongs to `Problem`. Stores `test_number`, `is_example`. (Raw inputs/outputs are not in DB, they go to storage).

## URLs & Views
- `GET /`: Dashboard.
- `GET /migrate/new/`: Form to enter Polygon ID and credentials.
- `POST /migrate/fetch/`: Fetches from Polygon API.
- `POST /migrate/commit/`: Saves to DB and uploads to Storage.

## Polygon API Authentication
- Authenticated via `POLYGON_API_KEY` and `POLYGON_API_SECRET`.
- Requests include an API signature (SHA512 hash of random string + endpoint + params + secret) as required by Codeforces Polygon.

## Redis Usage
- **Celery**: Redis is used as the message broker for Celery to process large test-case uploads asynchronously in the background.
- **Cache**: Used for caching fetched problem metadata to avoid hitting Polygon rate limits during the review stage.

## Cloud Storage (Azure/S3)
- Currently, Azure upload logic is tightly coupled into the migration view. It leaks into `views.py`.
- We will refactor this into `migration.storage.factory` to support S3/R2 transparently.

## Environment Variables
- `SECRET_KEY`, `DEBUG`, `DATABASE_URL`, `REDIS_URL`
- `POLYGON_API_KEY`, `POLYGON_API_SECRET`
- `STORAGE_PROVIDER` (azure | s3 | r2 | local)
- `AZURE_CONNECTION_STRING`, `AZURE_CONTAINER_NAME`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_ENDPOINT_URL`
