from django.shortcuts import render, get_object_or_404
from .models import Blog, Comment, Tag
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .forms import CreateCommentModelForm, CreateUserForm, CreateBlogModelForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.
def index(request):

	blog_nums = Blog.objects.all().count()
	user_nums = User.objects.all().count()
	visits_nums = request.session.get("visits_nums", 0)
	request.session["visits_nums"] = visits_nums + 1

	return render(
		request,
		'index.html',
		context={
			'blog_nums':blog_nums, 
			'user_nums':user_nums,
			'visits_nums':visits_nums
			}
	)

class BlogListView(generic.ListView):
	model = Blog
	paginate_by = 3

class UserListView(generic.ListView):
	model = User
	template_name = "ismblog/user_list.html"

	def get_queryset(self):
		return User.objects.filter(is_superuser=0)

class UserDetailView(generic.DetailView):
	model = User
	template_name = "ismblog/user_detail.html"

class UserUpdate(LoginRequiredMixin, UpdateView):
	model = User
	template_name = "ismblog/user_form.html"
	fields = ["username", "first_name", "last_name"]


class BlogDetailView(generic.DetailView):
	model = Blog

class BlogCreate(LoginRequiredMixin, CreateView):
	model = Blog
	fields = ['title', 'summary', 'content', 'tags']
	success_url = reverse_lazy('blogs')

class BlogDelete(LoginRequiredMixin, DeleteView):
	model = Blog
	success_url = reverse_lazy('blogs')

class BlogUpdate(LoginRequiredMixin, UpdateView):
	model = Blog
	fields = ['title', 'summary', 'content', 'tags']


# class CommentCreate(LoginRequiredMixin, CreateView):
#     model = Comment
#'
#     # success_url = reverse_lazy('blog-detail', args=str(blog.id))
#     success_url = reverse_lazy('users')
#     fields = ['content']

@login_required()
def create_blog(request):

	if request.method == "POST":

		form = CreateBlogModelForm(request.POST)

		if form.is_valid():
			form = form.save(commit=False)
			form.user = request.user
			form.username = request.user.username
			form.save()

			return HttpResponseRedirect(reverse('blogs'))

	else:
		form = CreateBlogModelForm()

	return render(
		request,
		template_name = "ismblog/blog_form.html",
		context = {"form":form, }
	)    


@login_required()
def create_comment(request, pk):
	blog_info = get_object_or_404(Blog, pk=pk)

	if request.method == 'POST':
		form = CreateCommentModelForm(request.POST)

		if form.is_valid():
			form = form.save(commit=False)
			form.blog_title = blog_info.title
			form.blog_id = blog_info
			form.user_name = request.user.username
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
			username = user.cleaned_data["username"]
			password = user.cleaned_data["password1"]
			email = user.cleaned_data["email"]
			form = User.objects.create_user(username, email, password)

			return HttpResponseRedirect(reverse('blogs'))
	else:
		user = CreateUserForm()

	return render(
		request,
		template_name = "registration/register.html",
		context = {
			"form":user
		}
	)