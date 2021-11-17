
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all_posts/<str:name>", views.all_posts, name="all_posts"),
    path("user_details/<str:name>", views.user_details, name="user_details"),
    path("following", views.following, name="following"),
    path("edit_post/<int:id>", views.edit_post, name="edit_post"),

    # API route
    path("post", views.post, name="post"),
    path("details/<str:name>", views.details, name="details"),
    path("user_posts/<str:name>", views.user_posts, name="user_posts"),
    path("edit_post1", views.edit_post1, name="edit_post1"),
    path("like_unlike/<int:id>", views.like_unlike, name="like_unlike")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
