from django.urls import path
from .views import *

urlpatterns = [
    path('', news_list, name='news_list_all')
]