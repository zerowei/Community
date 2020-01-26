from django.shortcuts import render, redirect
from django.db.models import Q
from QA.models import Question

# Create your views here.


def search(request):
    if 'q' not in request.GET:
        return redirect('home')

    queryobject = request.GET.get('q').strip()

    if len(queryobject) == 0:
        return redirect('home')

    result = Question.objects.filter(Q(title__icontains=queryobject) | Q(description__icontains=queryobject))
    count = result.count()
    context = {
        'count': count,
        'questions': result
    }
    return render(request, 'search/result.html', context)
