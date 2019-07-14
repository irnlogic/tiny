
from django.urls import path
from django.urls import re_path

from . import views

## import functions in views.py, which make tiny url and retrieve original url
from .views import url_detail_view, make_tiny, get_original

urlpatterns = [
    path('', views.index, name='index'),
    path('favicon.ico/', views.index, name='index'),
    path('url/', url_detail_view, name='urldetail' ),
    re_path(r'^maketiny/(.+)', make_tiny, name='url_tiny'),  ## route for url shortening
    path('<tinycode>/', get_original, name='go'),    ## route to fetch orginal url
]



