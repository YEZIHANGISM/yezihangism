from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Blog, Comment

class CreateCommentModelForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['content', "user_name"]