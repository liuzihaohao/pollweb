from django.urls import path,include
from django.contrib import admin
from .views import *

poll_urlpatterns = [
    path('', root_page),
    path('list/', list_poll),
    path('add/', add_poll),
    path('<int:uid>/', admin.site.urls),
    path('<int:uid>/edit/', admin.site.urls),
    path('<int:uid>/del/', admin.site.urls),
]
