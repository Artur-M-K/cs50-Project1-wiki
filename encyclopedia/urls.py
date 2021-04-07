from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.wiki, name="wiki"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("randomEntry", views.randomEntry, name="randomEntry"),
    path("editEntry/<str:name>", views.editEntry, name="editEntry")
]
