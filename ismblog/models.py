from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
import uuid

# Create your models here.
class Tag(models.Model):

    name = models.CharField(max_length=200,
                           help_text='choose some tags for blog')

    def __str__(self):
        return self.name

class Topic(models.Model):

    title = models.CharField(max_length=200,
                             help_text='choose topic for blogs')

    def __str__(self):
        return self.title


# class User(models.Model):

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4,)
#     name = models.CharField(max_length=200)
#     email = models.EmailField(max_length=200)
#     password = models.CharField(max_length=12)
#     isadmin = models.BooleanField()
#     # image = models.ImageField()

#     def __str__(self):
#         return self.name


class Blog(models.Model):

    title = models.CharField(max_length=200)
    # content = models.TextField()
    content = RichTextUploadingField(config_name="content_config")
    publish_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=200, null=True)
    summary = models.TextField(max_length=1000)
    tags = models.ManyToManyField(Tag)
    topic = models.ForeignKey("Topic", on_delete=models.SET_NULL, null=True)
    # comment = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True)
    star = models.IntegerField(default=0)
    pageviews = models.IntegerField(default=0)

    class Meta:
        ordering = ["-publish_date"]
        # order_with_respect_to = "publish_date"

    def __str__(self):
        return self.title

    def display_tag(self):
        return ", ".join([tag.name for tag in self.tags.all()])

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])


class Comment(models.Model):

    # name = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    blog_id = models.ForeignKey('Blog', on_delete=models.SET_NULL, null=True)
    blog_title = models.CharField(max_length=200, null=True)
    # user_name = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    # blog_title = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200, null=True)
    # content = models.TextField(max_length=1000)
    content = RichTextUploadingField(max_length=1000, config_name="content_config") # 可以考虑给评论新增配置
    publish_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-publish_date"]

    def __str__(self):
        return "comment user: %s"%self.user_name