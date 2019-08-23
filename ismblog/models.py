from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Tag(models.Model):

    name = models.CharField(max_length=200,
                           help_text='choose some tags for blog')

    def __str__(self):
        return self.name


class Topic(models.Model):

    title = models.CharField(max_length=200)

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
    content = RichTextUploadingField(config_name="content_config")
    publish_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    tags = models.ManyToManyField(Tag)
    topic = models.ForeignKey("Topic", on_delete=models.SET_NULL, null=True)
    star = models.IntegerField(default=0)
    pageviews = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-publish_date"]
        # order_with_respect_to = "publish_date"

    def __str__(self):
        return self.title

    def display_tag(self):
        return ", ".join([tag.name for tag in self.tags.all()])
        # return self.tags.all()

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def auto_increment_views(self):
        self.pageviews += 1
        self.save(update_fields=["pageviews"])



class Comment(models.Model):

    blog = models.ForeignKey('Blog', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = RichTextUploadingField(max_length=1000, config_name="content_config") # 可以考虑给评论新增配置
    publish_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-publish_date"]

    def __str__(self):
        return "comment user: %s"%self.user_name


class Message(models.Model):

    content = RichTextUploadingField(max_length=1000, config_name='content_config')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "leave message date"%self.date