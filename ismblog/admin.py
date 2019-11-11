from django.contrib import admin
from .models import Blog, Comment, Tag, Topic, Message, Notes

# Register your models here.

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "id", "publish_date", "topic")
    list_filter = ("topic", "publish_date")

@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


