from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("feed", views.feed, name="feed"),
    path("feed/<int:post_id>/", views.load_comments, name="load_comments"),
    path("like/<int:post_id>/", views.toggle_like, name="toggle_like"),
    path("feed/add_post", views.add_post, name="add_post"),
    path("login", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("signup", views.signup_view, name="signup_view")
]