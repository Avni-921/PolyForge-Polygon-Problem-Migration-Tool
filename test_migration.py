import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PolygonMigration.settings')
django.setup()

from django.test import Client
from problems.models import Problem, ProblemTestCase
from problems.storage import get_storage_backend

def run_migration():
    print("Testing Migration Flow...")
    from problems.polygon_api import PolygonAPI
    
    api = PolygonAPI()
    polygon_id = '69927'
    
    print(f"Fetching problem {polygon_id}...")
    info = api.get_problem_info(polygon_id)
    print("Problem Info:", info)
    
    print("Migrating to DB...")
    p, created = Problem.objects.update_or_create(
        polygon_id=polygon_id,
        defaults={'title': info.get('name', 'Unknown'), 'difficulty': 1}
    )
    print(f"Problem saved in DB: {p.title} (ID: {p.id})")
    
    print("Migrating test cases to Storage...")
    # This runs the logic we refactored
    api.migrate_to_azure_blob(
        problem_id=polygon_id,
        azure_account_url='',
        azure_tenant_id='',
        azure_client_id='',
        azure_username='',
        azure_password='',
        container_name='polyforge-test-cases',
        db_problem_id=p.id
    )

    # Verify Storage
    storage = get_storage_backend()
    prefix = f"test_cases/{p.id}/"
    files = storage.list_files(prefix)
    print(f"\nFiles successfully uploaded to Storage ({storage.__class__.__name__}): {len(files)}")
    for f in files[:10]: # Print first 10
        print(f" - {f}")
    if len(files) > 10:
        print(f" ... and {len(files) - 10} more.")

if __name__ == "__main__":
    run_migration()
