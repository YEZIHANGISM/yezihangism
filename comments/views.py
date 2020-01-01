from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment
from .forms import CreateCommentForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from ismblog.models import Blog
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
import datetime

# Create your views here.
@login_required()
def create_comment(request):
    referer = request.META.get("HTTP_REFERER", reverse("blogs"))
    comment_form = CreateCommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data["user"]
        comment.content = comment_form.cleaned_data["content"]
        comment.content_object = comment_form.cleaned_data["content_object"]
        comment.save()
        
        data = {}
        data["status"] = "SUCCESS"
        data["username"] = comment.user.username
        now = datetime.datetime.now()
        data["comment_time"] = "{year}年{month}月{day}日 {hour}:{minute}".format(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute)
        data["content"] = comment.content
    else:
        data = {}
        data["status"] = "ERROR"
        data["message"] = list(comment_form.errors.values())[0][0]

    return JsonResponse(data)