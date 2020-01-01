from django.urls import path, re_path
from comments import views

urlpatterns = [
    path('create_comment/', views.create_comment, name="create_comment"),
]