from django.forms import *
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Blog, Comment
from django.contrib.auth.models import User

class CreateCommentModelForm(ModelForm):

	class Meta:
		model = Comment
		fields = ['content']


class CreateUserForm(Form):

	username = CharField(max_length=150)
	password1 = CharField(max_length=128, widget=PasswordInput)
	password2 = CharField(max_length=128, widget=PasswordInput)
	email = EmailField(max_length=254, widget=EmailInput)

	def clean(self):
		cleaned_data = super().clean()
		username = cleaned_data.get("username")
		password1 = cleaned_data.get("password1")
		password2 = cleaned_data.get("password2")
		email = cleaned_data.get("email")

		if password1 != password2:
			raise ValidationError(_("Inconsistent password"))
		elif User.objects.filter(username=username):
			raise ValidationError(_("this username already in use"))
		elif User.objects.filter(email=email):
			raise ValidationError(_("the email already in use"))


		return cleaned_data

class CreateBlogModelForm(ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'summary', 'content', 'tags', 'topic']