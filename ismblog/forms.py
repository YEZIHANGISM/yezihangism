from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Blog, Message
from django.contrib.auth.models import User



class CreateUserForm(forms.Form):

	username = forms.CharField(label="用户名", 
							   max_length=150, 
							   widget=forms.TextInput(
								   attrs={"class":"form-control", 'placeholder':"请输入用户名"}
								))
	password1 = forms.CharField(label="密码", 
								max_length=128, 
								widget=forms.PasswordInput(
									attrs={"class":"form-control", 'placeholder':"请输入密码"}
								))
	password2 = forms.CharField(label="密码确认", 
								max_length=128, 
								widget=forms.PasswordInput(
									attrs={"class":"form-control", 'placeholder':"再次输入密码"}
								))
	email = forms.EmailField(label="邮箱", 
							 max_length=254, 
							 widget=forms.EmailInput(
								 attrs={"class":"form-control", 'placeholder':"请输入邮箱"}
							 ))

	def clean(self):
		cleaned_data = super().clean()
		username = cleaned_data.get("username")
		password1 = cleaned_data.get("password1")
		password2 = cleaned_data.get("password2")
		email = cleaned_data.get("email")

		if password1 != password2:
			raise ValidationError(_("密码不一致！！！"))
		elif User.objects.filter(username=username):
			raise ValidationError(_("用户名已存在"))
		elif User.objects.filter(email=email):
			raise ValidationError(_("邮箱已被使用"))


		return cleaned_data

class CreateBlogModelForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'content', 'tags', 'topic']


class LeaveMsgModelForm(forms.ModelForm):

	class Meta:
		model = Message
		fields = ['content']