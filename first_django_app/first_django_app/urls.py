from django.contrib import admin
from django.urls import path
from chat.views import index, login_view, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', index, name='index'),
    path('login/', login_view, name='login_view'),
    path('register/', register_view, name='register_view'),
]
