from django.shortcuts import render, get_object_or_404
from .models import Blog, Comment, Tag, Topic, Message
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy as _, reverse
from .forms import CreateCommentModelForm, CreateUserForm, CreateBlogModelForm, LeaveMsgModelForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.http import Http404

# Create your views here.

class BlogListView(generic.ListView):
	model = Blog
	paginate_by = 10

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

	# def post(self, request):
	# 	pk = self.kwargs.get("pk")
	# 	blog = Blog.objects.get(id=pk)
	# 	form = CreateCommentModelForm(request.POST)
	# 	if form.is_valid():
	# 		form = form.save(commit=False)
	# 		form.blog = blog.id
	# 		form.user = self.request.user
	# 		form.save()
	# 		return HttpResponseRedirect(reverse('blog-detail', args=str(blog.id)))


	def get_context_data(self, **kwargs):
		context = super(BlogDetailView, self).get_context_data(**kwargs)
		blog_list = BlogListView()
		queryset = blog_list.get_queryset()
		self.current_id = context["blog"].id
		self.current_topic = context["blog"].topic
		self.first_id = Blog.objects.all().order_by("id").first().id
		self.last_id = Blog.objects.all().order_by("id").last().id
		if self.has_previous():
			context["previous"] = Blog.objects.filter(id__lt=self.current_id).filter(topic__exact=self.current_topic).order_by("id").last()
		if self.has_next():
			context["next"] = Blog.objects.filter(id__gt=self.current_id).filter(topic__exact=self.current_topic).order_by("id").first()

		form = CreateCommentModelForm(self.request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.blog = context["blog"].id
			form.user = self.request.user
			form.save()

			return HttpResponseRedirect(reverse('blog-detail', args=str(context["blog"].id)))
		context["form"] = form
		context["blog_list"]= queryset

		return context


	def has_next(self):
		return self.current_id < self.last_id

	def has_previous(self):
		return self.current_id > 1

	def get_object(self):
		model = super(BlogDetailView, self).get_object()
		model.auto_increment_views()
		return model

	# def get_queryset(self):
	# 	qs = super(BlogDetailView, self).get_queryset()
	# 	pk = self.kwargs.get("pk")
	# 	# model = Blog.objects.get(id=pk)
	# 	model = Blog.objects.all()
	# 	model = self.get_object(model)
	# 	model.auto_increment_views()
	# 	return model


class BlogDelete(LoginRequiredMixin, DeleteView):
	model = Blog
	success_url = _('blogs')

class BlogUpdate(LoginRequiredMixin, UpdateView):
	model = Blog
	fields = ['title', 'content', 'tags', 'topic']


class TopicListView(generic.ListView):
	model = Topic

class MsgListView(generic.ListView):
	model = Message


def topic_blog_list(request, pk):
	blog = Blog.objects.filter(topic=pk)
	return render(
		request,
		template_name="ismblog/blog_list.html",
		context={
			"blog_list": blog,
		}
	)

# class CommentCreate(LoginRequiredMixin, CreateView):
#     model = Comment
#     # success_url = _('blog-detail', args=str(blog.id))
#     success_url = _('users')
#     fields = ['content']

@login_required()
def create_blog(request):

	if request.method == "POST":

		form = CreateBlogModelForm(request.POST)

		if form.is_valid():
			form = form.save(commit=False)
			form.user = request.user
			# form.username = request.user.username
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
			form.blog = blog_info
			form.user = request.user
			form.save()

			return HttpResponseRedirect(reverse('blog-detail', args=str(blog_info.id)))
	else:
		form = CreateCommentModelForm()

	return render(
		request,
		template_name='ismblog/comment_form.html',
		context={"form":form, "blog":blog_info}
	)

class LeavemsgView(generic.CreateView):

	form_class = LeaveMsgModelForm
	template_name = "ismblog/message_form.html"
	success_url = _('blogs')


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
		empty = "请输入搜索关键词！"

	blog = Blog.objects.filter(title__icontains=name)

	# 函数视图中的分页可参考如下，其中传递给模板的"blog_list"应该取分页后得到的数据page.object_list
	# paginator = Paginator(blog, 3)
	# page_kwarg = "page"
	# page = request.GET.get(page_kwarg,1)
	# page = paginator.get_page(page)

	return render(
		request,
		template_name="ismblog/blog_list.html",
		context={
			"blog_list": blog,
			"empty": empty
		}
	)


def filter_by_tag(request, pk):
	Tags = get_object_or_404(Tag, pk=pk)
	blog = Blog.objects.filter(tags=Tags.id)

	return render(
		request,
		template_name="ismblog/blog_list.html",
		context={
			"blog_list":blog
		}
	)

