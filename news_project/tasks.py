from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta

from .models import *


@shared_task
def send_email_task(pk):
    post = Post.objects.get(pk=pk)
    categories = post.postCategory.all()
    title = post.title
    subscriber_emails = []

    for category in categories:
        subscriber = category.subscribers.all()
        subscriber_emails += [sub.email for sub in subscriber]

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': f'{post.title}',
            'link': f'http://127.0.0.1:8000/posts/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=None,
        to=set(subscriber_emails),
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_send_email_task():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(autoDate__gte=last_week)
    categories = set(posts.values_list('postCategory__categoryName', flat=True))
    subscribers = User.objects.filter(categories__categoryName__in=categories)

    for sub in subscribers:
        html_content = render_to_string(
            'daily_post.html',
            {
                'link': 'http://127.0.0.1:8000/',
                'posts': posts,
                'user': sub.username
            }
        )
        msg = EmailMultiAlternatives(
            subject='Посты за неделю',
            body='',
            from_email=None,
            to=[sub.email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

