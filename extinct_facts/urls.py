from django.urls import path
from . import views

app_name = 'extinct_facts'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/get-extinct-fact/', views.get_extinct_fact, name='get_extinct_fact'),
    path('api/get-latest-news/', views.get_latest_news, name='get_latest_news'),
]
