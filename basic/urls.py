from django.urls import path,include
from django.contrib import admin
from .views import *

root_urlpatterns = [
    path('/', index),
    path('', index),
    path('login/', login),
    path('change_password/', change_password),
    path('logout/', logout),
    path('register/', register),
    path('del_user/', admin.site.urls),
]

log_db_urlpatterns = [
    path('', view_log),
]

user_db_urlpatterns = [
    path('list/', admin.site.urls),
    path('add/', admin.site.urls),
    path('<int:uid>/', admin.site.urls),
    path('<int:uid>/edit/', admin.site.urls),
    path('<int:uid>/del/', admin.site.urls),
]

group_db_urlpatterns = [
    path('list/', admin.site.urls),
    path('add/', admin.site.urls),
    path('<int:uid>/', admin.site.urls),
    path('<int:uid>/edit/', admin.site.urls),
    path('<int:uid>/del/', admin.site.urls),
]

basic_urlpatterns = [
    path('', basic_admin),
    path('log/', include(log_db_urlpatterns)),
    path('user/', include(user_db_urlpatterns)),
    path('group/', include(group_db_urlpatterns)),
]
