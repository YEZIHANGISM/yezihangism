from django.shortcuts import render, get_object_or_404
from .models import Blog, Comment, Tag, Topic
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .forms import CreateCommentModelForm, CreateUserForm, CreateBlogModelForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

	def get_context_data(self, **kwargs):
		context = super(BlogListView, self).get_context_data(**kwargs)
		context["tags"] = Tag.objects.all()
		return context

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

	def get_context_data(self, **kwargs):
		context = super(BlogDetailView, self).get_context_data(**kwargs)
		self.current_id = context["blog"].id
		self.first_id = Blog.objects.all().order_by("id").first().id
		self.last_id = Blog.objects.all().order_by("id").last().id
		if self.has_previous():
			context["previous"] = Blog.objects.filter(id__lt=self.current_id).order_by("id").last()
		if self.has_next():
			context["next"] = Blog.objects.filter(id__gt=self.current_id).order_by("id").first()

		return context

	def has_next(self):
		return self.current_id < self.last_id

	def has_previous(self):
		return self.current_id > 1


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

def search(request):
	empty = ""
	# search是input中的name
	name = request.GET.get('search')
	if name == "":
		empty = "search word is required"

	blog = Blog.objects.filter(title__icontains=name)

	return render(
		request,
		"ismblog/blog_list.html",
		context={
			"blog_list":blog,
			"empty": empty,
		}
	)

def filter_by_tag(request, pk):
	Tags = get_object_or_404(Tag, pk=pk)
	blog = Blog.objects.filter(tags=Tags.id)

	return render(
		request,
		"ismblog/blog_list.html",
		context={
			"blog_list":blog
		}
	)

def topic_list(request, pk):
	topic = get_object_or_404(Topic, pk=pk)
	print(topic)
	blog = Blog.objects.filter(topic=topic.id)

	return render(
		request,
		"ismblog/blog_list.html",
		context={
			"blog_list":blog
		}
	)