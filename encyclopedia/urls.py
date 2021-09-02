from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("wiki/", views.random, name="random"),
    path("wiki/wiki/", views.random, name="random"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/edit", views.edit, name="edit")
 
]
