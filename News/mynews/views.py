from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import EmailNewsForm, CommentForm
from django.core.mail import send_mail


def news_list(request):
    news = News.objects.all()
    return render(request, 'mynews/news_list_all.html', context={'news': news})


def news_detail(request, year, month, day, slug):
    new = get_object_or_404(News, slug=slug, status='published', time_publish__year=year, time_publish__month=month,
                            time_publish__day=day)
    comments = new.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = new
            new_comment.save()
    else:
        comment_form = CommentForm
    return render(request, 'mynews/news_detail.html', context={'new': new,
                                                               'comments': comments,
                                                               'new_comment': new_comment,
                                                               'comment_form': comment_form})


def news_share(request, news_id):
    new = get_object_or_404(News, id=news_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailNewsForm(request.POST)
        if form.is_valid():
            print('lul')
            cd = form.cleaned_data
            news_url = request.build_absolute_uri(new.get_absolute_url())
            subject = '{} ({}) recommended you this news "{}"'.format(cd['name'], cd['email'], new.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(new.title, news_url, cd['name'], cd['comment'])
            send_mail(subject, message, cd['email'], [cd['to']])
            sent = True
    else:
        form = EmailNewsForm()
    return render(request, 'mynews/email_form.html', context={'new': new, 'form': form, 'sent': sent})


