from django.urls import path
from ismblog import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path("", cache_page(60)(views.HomeListView.as_view()), name="home"),
    # path("", views.HomeListView.as_view(), name="home"),
	path("blogs/", views.BlogListView.as_view(), name='blogs'),
    # path("management/", views.index, name="index"),
    
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
    path("filter/<int:pk>", views.filter_by_tag, name="filter"),

    path("topic/", views.TopicListView.as_view(), name="topic"),
    path("topic/<int:pk>", views.topic_blog_list, name="topic-blog"),

    path("leavemsg/", views.LeavemsgView.as_view(), name='leavemsg'),
    path("msglist/", views.MsgListView.as_view(), name="messages"),

    path("notes/", views.NotesView.as_view(), name="notes"),

    path("star/<int:pk>", views.star_incr, name="star"),
    path("unstar/<int:pk>", views.unstar_decr, name="unstar")
]