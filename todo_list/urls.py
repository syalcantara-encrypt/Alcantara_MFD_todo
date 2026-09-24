from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("edit/<int:todo_id>/", views.edit_todo, name="edit_todo"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
