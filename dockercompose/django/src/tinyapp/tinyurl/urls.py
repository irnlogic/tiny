
from django.urls import path
from django.urls import re_path

from . import views

from .views import url_detail_view, make_tiny, get_original

urlpatterns = [
    path('', views.index, name='index'),
    path('url/', url_detail_view, name='urldetail' ),
    #path('maketiny/<url>', make_tiny, name='url_tiny'),
    re_path(r'^maketiny/(.+)', make_tiny, name='url_tiny'),
    path('<tinycode>/', get_original, name='go'),    
]



