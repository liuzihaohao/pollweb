from django.urls import path,include
from django.contrib import admin

poll_urlpatterns = [
    path('', admin.site.urls),
    path('list/', admin.site.urls),
    path('add/', admin.site.urls),
    path('<int:uid>/', admin.site.urls),
    path('<int:uid>/edit/', admin.site.urls),
    path('<int:uid>/del/', admin.site.urls),
]
