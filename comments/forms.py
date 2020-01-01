from django import forms
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget

class CreateCommentForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        if "user" in kwargs:
            self.user = kwargs.pop("user")
        super(CreateCommentForm, self).__init__(*args, **kwargs)

    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(widget=CKEditorWidget(config_name="short-config"), error_messages={"required": "评论内容不能为空"})

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data["user"] = self.user
        else:
            raise forms.ValidationError("用户未登录")

        content_type = self.cleaned_data["content_type"]
        object_id = self.cleaned_data["object_id"]
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk = object_id)
            self.cleaned_data["content_object"] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError("评论对象不存在")

        return self.cleaned_data