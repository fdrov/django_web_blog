from django.db.models import F
from django.views.generic import ListView, DetailView

from .models import Post, Category, Tag


class HomeListView(ListView):
    model = Post
    # queryset = get_list_or_404(Post, category__pk=6)
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    # def get_context_data(self, *, object_list=None, **kwargs):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Classic blog design'
        context['page_range'] = context['paginator'].get_elided_page_range(context['page_obj'].number, on_each_side=1,
                                                                           on_ends=1)
        return context


class PostsByCategory(ListView):
    template_name = 'blog/posts_by_category.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByTag(ListView):
    model = Post
    context_object_name = 'posts'
    allow_empty = False
    template_name = 'blog/posts_by_category.html'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегу: ' + Tag.objects.get(slug=self.kwargs['slug']).title
        print(type(Tag.objects.get(slug=self.kwargs['slug'])))
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context
