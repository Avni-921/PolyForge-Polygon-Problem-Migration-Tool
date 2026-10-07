"""
seed_questions.py
=================
Seeds the database with well-known Codeforces problems for demo purposes.
Run once:  python seed_questions.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PolygonMigration.settings')
django.setup()

from questions.models import CodeforcesQuestion

# 15 classic Codeforces problems across all difficulty levels
DEMO_QUESTIONS = [
    {
        "title": "A+B Problem",
        "url": "https://codeforces.com/problemset/problem/1/A",
        "difficulty": "easy",
        "tags": "math, implementation",
        "statement": (
            "Given two integers A and B, print their sum.\n\n"
            "Input: Two integers A and B (0 ≤ A, B ≤ 10^9) on a single line.\n"
            "Output: Print A + B."
        ),
    },
    {
        "title": "Watermelon",
        "url": "https://codeforces.com/problemset/problem/4/A",
        "difficulty": "easy",
        "tags": "math, brute force",
        "statement": (
            "Pete and Billy want to divide a watermelon of weight W kg into two parts, "
            "each weighing an even number of kilograms.\n\n"
            "Input: One integer W (1 ≤ W ≤ 100).\n"
            "Output: Print 'YES' if possible, 'NO' otherwise."
        ),
    },
    {
        "title": "Way Too Long Words",
        "url": "https://codeforces.com/problemset/problem/71/A",
        "difficulty": "easy",
        "tags": "strings, implementation",
        "statement": (
            "Abbreviate each word that is strictly longer than 10 characters to "
            "<first_letter><number_of_omitted_letters><last_letter>.\n\n"
            "Input: First line n (1 ≤ n ≤ 100), then n words each of length ≤ 100.\n"
            "Output: Print abbreviated versions."
        ),
    },
    {
        "title": "Beautiful Matrix",
        "url": "https://codeforces.com/problemset/problem/364/A",
        "difficulty": "easy",
        "tags": "implementation, sortings",
        "statement": (
            "A 5×5 matrix is 'beautiful' if the number 5 is in the center. "
            "Find the minimum number of moves (shifting 5 up/down/left/right) to make it beautiful.\n\n"
            "Input: 5×5 matrix of integers 1..25 (each exactly once).\n"
            "Output: Minimum moves."
        ),
    },
    {
        "title": "Team",
        "url": "https://codeforces.com/problemset/problem/231/A",
        "difficulty": "easy",
        "tags": "greedy, implementation",
        "statement": (
            "Petya, Vasya and Tonya are on a team. For each problem, each member votes YES (1) or NO (0). "
            "Count problems where at least 2 members vote YES.\n\n"
            "Input: n (1 ≤ n ≤ 1000), then n lines each with 3 integers.\n"
            "Output: Number of problems they will solve."
        ),
    },
    {
        "title": "Stones on the Table",
        "url": "https://codeforces.com/problemset/problem/266/A",
        "difficulty": "easy",
        "tags": "implementation",
        "statement": (
            "There are n stones on a table. Each stone has a color — 'W' or 'B'. "
            "Repeatedly remove the rightmost stone if it matches the one before it. "
            "Count how many you removed.\n\n"
            "Input: n, then string of n characters 'W'/'B'.\n"
            "Output: Number of removals."
        ),
    },
    {
        "title": "Codeforces Round Sequence",
        "url": "https://codeforces.com/problemset/problem/828/A",
        "difficulty": "easy",
        "tags": "math, implementation",
        "statement": (
            "A sequence is called 'almost arithmetic' if the difference between consecutive terms "
            "changes by at most 1. Given the first two elements, find the minimum and maximum possible "
            "n-th element.\n\n"
            "Input: Integers a, b, n.\n"
            "Output: Two integers: min and max values of the n-th element."
        ),
    },
    {
        "title": "Kicker",
        "url": "https://codeforces.com/problemset/problem/939/A",
        "difficulty": "easy",
        "tags": "implementation",
        "statement": (
            "Two teams played a kicker match. Team 1 has players A and B; Team 2 has C and D. "
            "Given the match score, determine the winner or print 'Friendship'.\n\n"
            "Input: Four names and a score like '2:1'.\n"
            "Output: Winner's names or 'Friendship'."
        ),
    },
    {
        "title": "Bit++",
        "url": "https://codeforces.com/problemset/problem/282/A",
        "difficulty": "easy",
        "tags": "implementation",
        "statement": (
            "In Bit++ language X++ increases X by 1 and --X decreases X by 1. "
            "Given a sequence of operations, print the final value of X starting from 0.\n\n"
            "Input: n and n strings like '++X' or 'X--'.\n"
            "Output: Final value of X."
        ),
    },
    {
        "title": "Gravity Flip",
        "url": "https://codeforces.com/problemset/problem/405/A",
        "difficulty": "easy",
        "tags": "sortings, implementation",
        "statement": (
            "A box contains n columns of cubes. When you flip the box to the right, "
            "cubes fall to the right side. Print the resulting column heights.\n\n"
            "Input: n, then n integers (column heights).\n"
            "Output: Column heights after flipping (sorted ascending)."
        ),
    },
    {
        "title": "Next Round",
        "url": "https://codeforces.com/problemset/problem/589/A",
        "difficulty": "easy",
        "tags": "implementation, *special problem",
        "statement": (
            "In a round, k participants advance. The k-th place score is the cutoff. "
            "Count how many participants advance (score > 0 AND score ≥ cutoff).\n\n"
            "Input: n, k, then n scores in non-increasing order.\n"
            "Output: Number of participants who advance."
        ),
    },
    {
        "title": "Petya and Strings",
        "url": "https://codeforces.com/problemset/problem/96/A",
        "difficulty": "medium",
        "tags": "strings, implementation",
        "statement": (
            "Compare two strings s and t lexicographically, but treat uppercase and lowercase letters "
            "as equal. Print -1, 0, or 1 accordingly.\n\n"
            "Input: Two strings of the same length (up to 100 chars).\n"
            "Output: -1, 0, or 1."
        ),
    },
    {
        "title": "Queue at the School",
        "url": "https://codeforces.com/problemset/problem/266/B",
        "difficulty": "medium",
        "tags": "implementation, simulation",
        "statement": (
            "A queue of boys (B) and girls (G). Each second every B-G adjacent pair swaps. "
            "Print the queue after t seconds.\n\n"
            "Input: n, t, then the initial queue string.\n"
            "Output: Queue after t seconds."
        ),
    },
    {
        "title": "Dijkstra on Large Graphs",
        "url": "https://codeforces.com/problemset/problem/20/C",
        "difficulty": "hard",
        "tags": "graphs, shortest paths, dijkstra",
        "statement": (
            "Given a directed weighted graph with n nodes and m edges, find the shortest "
            "path from vertex 1 to vertex n. Print the path length or -1 if unreachable.\n\n"
            "Input: n, m, then m lines: u v w.\n"
            "Output: Minimum distance or -1."
        ),
    },
    {
        "title": "Palindrome Partition",
        "url": "https://codeforces.com/problemset/problem/906/E",
        "difficulty": "hard",
        "tags": "dp, strings, palindromes",
        "statement": (
            "Partition string s into k substrings such that the i-th substring concatenated with "
            "the reverse of the (k+1-i)-th substring is a palindrome. Find minimum k or -1.\n\n"
            "Input: String s (|s| ≤ 4000).\n"
            "Output: Minimum k or -1."
        ),
    },
]


def seed():
    created = 0
    updated = 0
    for q in DEMO_QUESTIONS:
        obj, was_created = CodeforcesQuestion.objects.update_or_create(
            title=q["title"],
            defaults={
                "url": q["url"],
                "difficulty": q["difficulty"],
                "tags": q["tags"],
                "statement": q["statement"],
            }
        )
        if was_created:
            created += 1
        else:
            updated += 1

    total = CodeforcesQuestion.objects.count()
    print(f"\nSEEDING COMPLETE!")
    print(f"   Created : {created}")
    print(f"   Updated : {updated}")
    print(f"   Total in DB: {total}")
    print(f"\nQuestions now in DB:")
    for q in CodeforcesQuestion.objects.all().order_by('difficulty', 'title'):
        print(f"  [{q.difficulty.upper():6}]  {q.title}")


if __name__ == "__main__":
    seed()
