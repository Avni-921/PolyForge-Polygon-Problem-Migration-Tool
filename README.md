# PolyForge - Polygon Problem Migration Tool

PolyForge is a Django-based web application that migrates competitive programming problems from Codeforces Polygon directly into an internal PostgreSQL database (structured metadata) and a scalable Cloud Storage bucket (unstructured test case files).

## Architecture
- **Django**: Core web framework and API integration.
- **PostgreSQL**: Stores Problem, Tag, and TestCase counts.
- **Cloud Storage (S3/Azure)**: Stores massive test-case inputs (`tests/01`) and expected outputs (`tests/01.a`).

## Prerequisites
- Python 3.12+
- Docker (for PostgreSQL & Redis)
- Polygon API Keys

## Setup
1. Clone the repository and navigate into it.
2. Run `make setup` to install dependencies in a virtual environment.
3. Copy `.env.example` to `.env` and fill in your keys.
4. Run `make up` to start PostgreSQL and Redis via Docker.
5. Run `make migrate` to create database tables.
6. Run `make run` to start the server.

## Obtaining Polygon API Keys
1. Create an account at https://polygon.codeforces.com/
2. Go to **Settings** -> **API**.
3. Generate a new key and secret. Add these to your `.env` file as `POLYGON_API_KEY` and `POLYGON_API_SECRET`.

## Storage Providers
You can configure where test cases are uploaded by setting `STORAGE_PROVIDER` in `.env`:
- `local`: Saves to `./local_storage/` (great for testing without internet).
- `s3`: Requires `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`.
- `r2`: Set `STORAGE_PROVIDER=r2` and provide `AWS_S3_ENDPOINT_URL`.
- `azure`: Requires `AZURE_CONNECTION_STRING` and `AZURE_CONTAINER_NAME`.

## Troubleshooting
| Issue | Fix |
|-------|-----|
| `make up` fails | Ensure Docker Desktop is running on your machine. |
| Check setup fails Redis | Ensure port 6379 is not used by another local Redis instance. |
| Storage upload fails | Verify your AWS/Azure credentials and bucket name in `.env`. |

## How the Migration Works
1. **Fetch**: The app securely hashes a request to Polygon and downloads problem data.
2. **Review**: You review the test count, name, and manually assign a difficulty and 2 tags.
3. **Migrate**: The problem is saved to PostgreSQL, and old test cases are cleared to ensure idempotency (no duplicates).
4. **Upload**: Test cases are streamed directly into your chosen Cloud Storage provider.
