from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CodeforcesQuestion


@login_required(login_url='/users/login/')
def question_list(request):
    """Shows all Codeforces questions grouped by difficulty."""
    difficulty = request.GET.get('difficulty', '')
    search = request.GET.get('search', '').strip()

    qs = CodeforcesQuestion.objects.all().order_by('difficulty', 'title')

    if difficulty:
        qs = qs.filter(difficulty=difficulty)
    if search:
        qs = qs.filter(title__icontains=search)

    context = {
        'questions': qs,
        'difficulty_filter': difficulty,
        'search': search,
        'easy_count': CodeforcesQuestion.objects.filter(difficulty='easy').count(),
        'medium_count': CodeforcesQuestion.objects.filter(difficulty='medium').count(),
        'hard_count': CodeforcesQuestion.objects.filter(difficulty='hard').count(),
        'total_count': CodeforcesQuestion.objects.count(),
    }
    return render(request, 'questions/list.html', context)


@login_required(login_url='/users/login/')
def question_detail(request, pk):
    """Shows a single Codeforces question with full statement and a link to solve it."""
    question = get_object_or_404(CodeforcesQuestion, pk=pk)
    tags_list = [t.strip() for t in question.tags.split(',') if t.strip()]
    context = {
        'question': question,
        'tags_list': tags_list,
    }
    return render(request, 'questions/detail.html', context)
