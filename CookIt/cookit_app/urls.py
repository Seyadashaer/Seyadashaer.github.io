from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.index),
    path('home', views.home),
    path('login_page', views.login_page),
    path("register_page", views.register_page),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path("my_reciepes", views.my_reciepes),
    path("all_reciepes", views.all_reciepes),
    path("category_reciepes", views.category_reciepes),
    path("add_reciepe_page", views.add_reciepe_page),
    path("reciepe_details", views.reciepe_details),
    path("categories", views.categories),
    path("add_recipe", views.add_recipe),

]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
