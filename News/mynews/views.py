from django.shortcuts import render


def news_list(request):
    return render(request, 'mynews/news_list_all.html')
