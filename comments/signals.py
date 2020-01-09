from django.db.models.signals import post_save
from notifications.signals import notify
from comments.models import Comment
from django.dispatch import receiver

@receiver(post_save, sender=Comment)
def send_notifications(sender, instance, **kwargs):
    recipient = instance.content_object.user
    blog = instance.content_object
    verb = "{user}评论了你的博客 <{blog}>".format(user=instance.user.username, blog=blog.title)

    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance)
