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
    path('list/', view_user),
    path('add/', add_user),
    path('<int:uid>/', view_one_user),
    path('<int:uid>/edit/', edit_user),
    path('<int:uid>/del_active/', del_active_user),
    path('<int:uid>/del/', del_user),
]

basic_urlpatterns = [
    path('', basic_admin),
    path('log/', include(log_db_urlpatterns)),
    path('user/', include(user_db_urlpatterns)),
    path('group/', include(group_db_urlpatterns)),
]
