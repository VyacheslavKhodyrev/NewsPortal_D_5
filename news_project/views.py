from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, PostCategory, Category
from .filters import PostFilter
from .forms import NewsForm, ArticleForm
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from .tasks import send_email_task

class PostsList(ListView):
    model = Post
    ordering = '-autoDate'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostsSearch(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'search.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news_project.news_create'
    # raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'create_news.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.postType = 'NE'
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news_project.article_create'
    # raise_exception = True
    form_class = ArticleForm
    model = Post
    template_name = 'create_article.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.postType = 'AR'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news_project.news_update'
    # raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'create_news.html'


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news_project.article_update'
    # raise_exception = True
    form_class = ArticleForm
    model = Post
    template_name = 'create_article.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news_project.news_delete'
    # raise_exception = True
    model = Post
    template_name = 'delete_news.html'
    success_url = reverse_lazy('posts_list')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news_project.article_delete'
    # raise_exception = True
    model = Post
    template_name = 'delete_article.html'
    success_url = reverse_lazy('posts_list')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_posts_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-autoDate')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории '
    return render(request, 'subscribe.html', {'category': category, 'message': message})


class PostView(CreateView):
    def get(self, request, pk):
        send_email_task.delay()
        #return HttpResponse(content='html_content')
