# from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blog.models import Post


def post_list(request):
    post_list = Post.published.all()
    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found.")
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


class PostListView(ListView):
    """
    Альтернативное представление списка постов
    """
    # атрибут queryset используется для того, чтобы иметь конкретно-
    # прикладной набор запросов QuerySet, не извлекая все объекты. Вместо
    # определения атрибута queryset мы могли бы указать model=Post, и Django
    # сформировал бы для нас типовой набор запросов Post.objects.all()
    queryset = Post.published.all()
    # контекстная переменная posts используется для результатов запроса.
    # Если не указано имя контекстного объекта context_object_name, то по
    # умолчанию используется переменная object_list
    context_object_name = 'posts'
    paginate_by = 3
    # конкретно-прикладной шаблон используется для прорисовки страницы
    # шаблоном template_name. Если шаблон не задан, то по умолчанию ListView
    # будет использовать blog/post_list.html
    template_name = 'blog/post/list.html'
