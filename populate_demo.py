"""
Bulk-migrate all accessible Polygon problems into the DB and local storage.
This populates the app with real data for the demo video.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PolygonMigration.settings')
django.setup()

from problems.polygon_api import PolygonAPI
from problems.models import Problem, ProblemTag, SampleTestCase, ProblemTestCase
from problems.storage import get_storage_backend
from django.utils.text import slugify
import lxml.html
import re
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def parse_problem_html(html_content):
    """Parse Polygon problem.html and extract fields."""
    tree = lxml.html.fromstring(html_content)

    def get_div_inner_html(tree, class_name, skip_section_title=False):
        div = tree.xpath(f'//div[@class="{class_name}"]')
        if not div:
            return ''
        div = div[0]
        children = div.getchildren()
        html_parts = []
        for child in children:
            if skip_section_title and child.tag == 'div' and 'section-title' in child.get('class', ''):
                continue
            html_parts.append(lxml.html.tostring(child, encoding='unicode'))
        content = ''.join(html_parts).strip()
        content = re.sub(r'^(<p>\s*</p>)+', '', content)
        return content

    legend = get_div_inner_html(tree, 'legend')
    input_format = get_div_inner_html(tree, 'input-specification', skip_section_title=True)
    output_format = get_div_inner_html(tree, 'output-specification', skip_section_title=True)
    title = ''
    title_div = tree.xpath('//div[@class="title"]')
    if title_div:
        title = title_div[0].text_content().strip()
    notes = get_div_inner_html(tree, 'note', skip_section_title=True)
    return {
        'title': title,
        'legend': legend,
        'input_format': input_format,
        'output_format': output_format,
        'notes': notes,
    }

# Tag + difficulty presets for each problem to make the demo look polished
PROBLEM_PRESETS = {
    '69927': {
        'difficulty': 'easy',
        'tags': ['math', 'implementation'],
    },
    '69933': {
        'difficulty': 'medium',
        'tags': ['binary-search', 'interactive'],
    },
    '69943': {
        'difficulty': 'hard',
        'tags': ['binary-search', 'math', 'greedy'],
    },
    '208585': {
        'difficulty': 'easy',
        'tags': ['math', 'graders'],
    },
}

def migrate_problem(api, polygon_id, preset):
    """Migrate a single problem: metadata -> DB, test cases -> DB + storage."""
    print(f"\n{'='*60}")
    print(f"  Migrating Polygon Problem {polygon_id}")
    print(f"{'='*60}")

    # 1. Fetch problem info
    info = api.get_problem_info(polygon_id)
    print(f"  Time limit: {info.get('timeLimit')} ms, Memory: {info.get('memoryLimit')} MB")

    # 2. Download and parse the problem package HTML
    try:
        problem_html = api.download_and_extract_package(polygon_id)
        html_data = parse_problem_html(problem_html)
    except Exception as e:
        print(f"  WARNING: Could not download package: {e}")
        html_data = {'title': '', 'legend': '', 'input_format': '', 'output_format': '', 'notes': ''}

    title = html_data['title'] or info.get('name', f'Problem {polygon_id}')
    slug = slugify(title)
    # Ensure unique slug
    counter = 1
    original_slug = slug
    while Problem.objects.filter(slug=slug).exclude(polygon_id=polygon_id).exists():
        slug = f"{original_slug}-{counter}"
        counter += 1

    # 3. Get checker type
    try:
        checker_type = api._make_request('problem.checker', {'problemId': polygon_id}) or 'ncmp'
        if checker_type.startswith('std::'):
            checker_type = checker_type[5:]
        if checker_type.endswith('.cpp'):
            checker_type = checker_type[:-4]
        valid_checkers = ['ncmp', 'fcmp', 'hcmp', 'lcmp', 'nyesno', 'rcmp4', 'rcmp6', 'rcmp9', 'wcmp', 'yesno']
        if checker_type not in valid_checkers:
            checker_type = 'custom'
    except Exception:
        checker_type = 'ncmp'

    # 4. Get test case count
    try:
        test_list = api.get_test_cases(polygon_id)
        test_case_count = len(test_list)
    except Exception:
        test_case_count = 0

    # 5. Save to DB (update or create)
    problem_obj, created = Problem.objects.update_or_create(
        polygon_id=polygon_id,
        defaults={
            'title': title,
            'slug': slug,
            'difficulty': preset['difficulty'],
            'problem_statement': html_data['legend'],
            'input_format': html_data['input_format'],
            'output_format': html_data['output_format'],
            'notes': html_data['notes'],
            'time_limit': info.get('timeLimit', 1000),
            'memory_limit': info.get('memoryLimit', 256),
            'checker_type': checker_type,
            'test_case_count': test_case_count,
        }
    )
    action = "Created" if created else "Updated"
    print(f"  {action} in DB: '{title}' (ID: {problem_obj.id})")

    # 6. Add tags
    problem_obj.extra_tags.clear()
    for tag_name in preset['tags']:
        tag, _ = ProblemTag.objects.get_or_create(tag_name=tag_name)
        problem_obj.extra_tags.add(tag)
    print(f"  Tags: {', '.join(preset['tags'])}")

    # 7. Fetch all test cases and save to DB + storage
    print(f"  Fetching {test_case_count} test cases from Polygon API...")
    try:
        all_test_cases = api.get_all_test_cases(polygon_id)
    except Exception as e:
        print(f"  ERROR fetching test cases: {e}")
        all_test_cases = []

    if all_test_cases:
        # Clear old DB test cases for idempotency
        ProblemTestCase.objects.filter(problem=problem_obj).delete()
        SampleTestCase.objects.filter(problem=problem_obj).delete()

        storage = get_storage_backend()

        # Clear old storage files
        prefix = f"test_cases/{problem_obj.id}/"
        try:
            for key in storage.list_files(prefix):
                storage.delete_file(key)
        except Exception:
            pass

        sample_order = 1
        for idx, tc in enumerate(all_test_cases, start=1):
            inp = tc.get('input', '').rstrip()
            out = tc.get('output', '').rstrip()
            is_sample = tc.get('is_sample', False)

            if not inp and not out:
                continue

            # Save to ProblemTestCase (truncated to 260 chars for DB)
            ProblemTestCase.objects.create(
                problem=problem_obj,
                is_sample=is_sample,
                input=inp[:260],
                output=out[:260],
                description=tc.get('description', ''),
                order=idx
            )

            # Save samples to SampleTestCase too
            if is_sample:
                SampleTestCase.objects.create(
                    problem=problem_obj,
                    input=inp,
                    output=out,
                    order=sample_order
                )
                sample_order += 1

            # Upload full test case to storage
            input_key = storage.build_input_key(str(problem_obj.id), idx)
            output_key = storage.build_output_key(str(problem_obj.id), idx)
            storage.upload_file(input_key, inp.encode('utf-8'))
            storage.upload_file(output_key, out.encode('utf-8'))

        tc_count = ProblemTestCase.objects.filter(problem=problem_obj).count()
        sample_count = SampleTestCase.objects.filter(problem=problem_obj).count()
        storage_files = storage.list_files(prefix)
        print(f"  DB test cases: {tc_count} ({sample_count} samples)")
        print(f"  Storage files: {len(storage_files)} (in {prefix})")
    else:
        print(f"  No test cases fetched.")

    print(f"  DONE: {title}")
    return problem_obj


def main():
    api = PolygonAPI()

    # List all accessible problems
    print("Listing all accessible Polygon problems...")
    problems = api._make_request('problems.list', {})
    print(f"Found {len(problems)} problems:\n")
    for p in problems:
        pid = str(p['id'])
        print(f"  [{pid}] {p['name']} (owner: {p['owner']}, access: {p['accessType']})")

    # Migrate each problem that has a preset
    migrated = []
    for p in problems:
        pid = str(p['id'])
        if pid in PROBLEM_PRESETS:
            try:
                obj = migrate_problem(api, pid, PROBLEM_PRESETS[pid])
                migrated.append(obj)
            except Exception as e:
                print(f"\n  FAILED to migrate {pid}: {e}")

    # Final summary
    print(f"\n{'='*60}")
    print(f"  MIGRATION COMPLETE")
    print(f"{'='*60}")
    print(f"  Problems migrated: {len(migrated)}")
    for obj in migrated:
        tags = ', '.join([t.tag_name for t in obj.extra_tags.all()])
        tc = ProblemTestCase.objects.filter(problem=obj).count()
        print(f"    [{obj.polygon_id}] {obj.title} | {obj.difficulty} | {tc} tests | tags: {tags}")

    total_storage = get_storage_backend().list_files("test_cases/")
    print(f"\n  Total storage files: {len(total_storage)}")
    print(f"\n  Login: admin@test.com / admin123")
    print(f"  URL:   http://127.0.0.1:8000/")


if __name__ == '__main__':
    main()
