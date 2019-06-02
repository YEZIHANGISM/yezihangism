from django.contrib import admin
from .models import Blog, Comment, Tag, Topic

# Register your models here.

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
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
