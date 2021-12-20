from django.shortcuts import render
from django.views.generic import ListView

from .models import Post, Category


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
    template_name = 'blog/category.html'
    context_object_name = 'posts_by_category'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


def index(request):
    return render(request, 'blog/index.html')


def get_category(request, slug):
    return render(request, 'blog/category.html')


def get_post(request, slug):
    return render(request, 'blog/post.html')
