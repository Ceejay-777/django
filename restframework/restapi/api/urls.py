from django.urls import path
from . import views

urlpatterns = [
    path("blogposts/", views.BlogPostListCreate.as_view(), name="blogpost_create-view"),
    path("blogposts/get", views.BlogPostList.as_view(), name="blogpost_create-view-custom"),
    path("blogposts/<int:pk>/", views.BlogPostRetrieveUpdateDestroy.as_view(), name="update")
]

