
from django.urls import path
from . import views

from .views import url_detail_view, url_tiny, url_original

urlpatterns = [
    path('', views.index, name='index'),
    path('url/', url_detail_view, name='urldetail' ),
    path('originalurl/', url_original, name='url_original' ),
    path('tinyurl/', url_tiny, name='url_tiny' ),
]



