from django.urls import path
from ismblog import views

urlpatterns = [
	path("", views.BlogListView.as_view(), name='blogs'),
    path("management/", views.index, name="index"),
    
    path("users/", views.UserListView.as_view(), name="users"),
    path("user/<int:pk>", views.UserDetailView.as_view(), name="user-detail"),
    path("user/<int:pk>/update", views.UserUpdate.as_view(), name="user-update"),

    path("blog/<int:pk>", views.BlogDetailView.as_view(), name="blog-detail"),
    path("blog/<int:pk>/delete", views.BlogDelete.as_view(), name="blog-delete"),
    path("blog/<int:pk>/update", views.BlogUpdate.as_view(), name="blog-update"),

    path("createblog/", views.create_blog, name="blog-create"),
    path("comment/<int:pk>/create", views.create_comment, name="comment-create"),

    # path("register/", views.create_user, name="register"),

    path("search/", views.search, name="search"),
]