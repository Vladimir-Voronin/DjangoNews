from django.urls import path
from .views import *

urlpatterns = [
    path('', news_list, name='news_list_all'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', news_detail, name='news_detail'),
    path('<int:news_id>/share/', news_share, name='news_share')
]
