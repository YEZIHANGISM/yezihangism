from django.shortcuts import render, get_object_or_404
from .models import Blog, Comment, Tag
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .forms import CreateCommentModelForm, CreateUserForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.
def index(request):

    blog_nums = Blog.objects.all().count()
    user_nums = User.objects.all().count()

    return render(
        request,
        'index.html',
        context={'blog_nums':blog_nums, 'user_nums':user_nums}
    )

class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 3

class UserListView(generic.ListView):
    model = User
    template_name = "ismblog/user_list.html"

class UserDetailView(generic.DetailView):
    model = User
    template_name = "ismblog/user_detail.html"

class BlogDetailView(generic.DetailView):
    model = Blog

class BlogCreate(PermissionRequiredMixin, CreateView):
    model = Blog
    permission_required = 'ismblog.can_operate_blog'
    fields = ['title', 'summary', 'content', 'tags']
    success_url = reverse_lazy('blogs')

class BlogDelete(PermissionRequiredMixin, DeleteView):
    model = Blog
    permission_required = 'ismblog.can_operate_blog'
    success_url = reverse_lazy('blogs')

class BlogUpdate(PermissionRequiredMixin, UpdateView):
    model = Blog
    permission_required = 'ismblog.can_operate_blog'
    fields = ['title', 'summary', 'content', 'tags']


# class CommentCreate(PermissionRequiredMixin, CreateView):
#     model = Comment
#     permission_required = 'ismblog.can_mark_returned'
#     # success_url = reverse_lazy('blog-detail', args=str(blog.id))
#     success_url = reverse_lazy('users')
#     fields = ['content']


@login_required()
def create_comment(request, pk):
    blog_info = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        form = CreateCommentModelForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.blog_title = blog_info.title
            form.blog_id = blog_info
            # form.user_name = user.name
            form.save()

            return HttpResponseRedirect(reverse('blog-detail', args=str(blog_info.id)))

    else:
        form = CreateCommentModelForm()

    return render(
        request,
        template_name='ismblog/comment_form.html',
        context={"form":form, "blog":blog_info}
    )


def create_user(request):

    if request.method == "POST":
        user = CreateUserForm(request.POST)

        if user.is_valid():
            username = User.cleaned_data["username"]
            password1 = User.cleaned_data["password"]
            password2 = User.cleaned_data["password2"]
            email = User.cleaned_data["email"]
            form = User.objects.create_user(username, email, password1, password2)

            return HttpResponseRedirect(reverse("blogs/"))
    else:
        user = CreateUserForm()

    return render(
        request,
        template_name = "registration/register.html",
        context = {
            "user":user
        }
    )