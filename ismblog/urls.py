from django.urls import path
from ismblog import views

urlpatterns = [
	path("", views.index, name='index'),
    path("users/", views.UserListView.as_view(), name="users"),
    path("blogs/", views.BlogListView.as_view(), name="blogs"),

    path("user/<uuid:pk>", views.UserDetailView.as_view(), name="user-detail"),
    path("blog/<int:pk>", views.BlogDetailView.as_view(), name="blog-detail"),

    path("createblog/", views.BlogCreate.as_view(), name='blog-create'),
    path("blog/<int:pk>/delete", views.BlogDelete.as_view(), name="blog-delete"),
    path("blog/<int:pk>/update", views.BlogUpdate.as_view(), name="blog-update"),

    # path("comment/<int:pk>/create", views.CommentCreate.as_view(), name="comment-create"),
    path("comment/<int:pk>/create", views.create_comment, name="comment-create"),
]