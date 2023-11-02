from django.contrib import admin
from django.urls import path
from parkVision import views

urlpatterns = [
    path("", views.home, name="home"),
    path("features", views.features, name="Features"),
    path("generate", views.generate, name="Generate"),
    path("entry", views.entry, name="Entry"),
    path("manage", views.manage, name="Manage"),
    path("exit", views.exit, name="Exit"),
    path("scan", views.scan, name="Scan"),
    path("show", views.show, name="Show")
]