from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Blog, Comment
from django.contrib.auth.models import User

class CreateCommentModelForm(ModelForm):

	class Meta:
		model = Comment
		fields = ['content', "user_name"]


class CreateUserForm(ModelForm):

	class Meta:
		model = User
		fields = ["username", "password", "email"]