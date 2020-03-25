from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
import mistune
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
import re
from django.views.generic import ListView, DetailView
from django.db.models import Q
from pure_pagination.mixins import PaginationMixin


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.increase_views()

    # post.body = mistune.markdown(post.body)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        # 记得在顶部引入 TocExtension 和 slugify
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog/detail.html', context={'post': post})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        # 视图必须返回一个 HttpResponse 对象
        return response


# 可以简单地把 get 方法看成是 detail 视图函数，至于其它的像 get_object、get_context_data 都是辅助方法，
# 这些方法最终在 get 方法中被调用，
# 这里你没有看到被调用的原因是它们隐含在了 super(PostDetailView, self).get(request, *args, **kwargs)
# 即父类 get 方法的调用中。最终传递给浏览器的 HTTP 响应就是 get 方法返回的 HttpResponse 对象。


def index(request):
    # post_list = Post.objects.all().order_by('-created_time')
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 2


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    # post_list = Post.objects.filter(category=cate).order_by('-created_time')
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})


class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


def archive(request, year, month):
    # post_list = Post.objects.filter(created_time__year=year,
    #                                 created_time__month=month
    #                                 ).order_by('-created_time')
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )
    return render(request, 'blog/index.html', context={'post_list': post_list})
    # Python中调用属性的方式通常是created_time.year，
    # 但是由于这里作为方法的参数列表，所以django要求我们把点替换成了两个下划线，即created_time__year。


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year, created_time__month=month)

        # 记得导入 from django.db.models import Q
        # filter(Q(created_time__year=year) & Q(created_time__month=month))


# 它获取的是某个分类下的全部文章。因此 category 视图函数中多了一步，
# 在类视图中，从 URL 捕获的路径参数值保存在实例的 kwargs 属性（是一个字典）里，
# 非路径参数值保存在实例的 args 属性（是一个列表）里。
# 所以我们使了 self.kwargs.get('pk') 来获取从 URL 捕获的分类 id 值。
# 然后我们调用父类的 get_queryset 方法获得全部文章列表，紧接着就对返回的结果调用了 filter 方法来筛选该分类下的全部文章并返回。

# 此外我们可以看到 CategoryView 类中指定的属性值和 IndexView 中是一模一样的，所以如果为了进一步节省代码，甚至可以直接继承 IndexView
# class CategoryView(IndexView):
#     def get_queryset(self):
#         cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
#         return super(CategoryView, self).get_queryset().filter(category=cate)


def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    # post_list = Post.objects.filter(tags=t).order_by('-created_time')
    post_list = Post.objects.filter(tags=t)
    return render(request, 'blog/index.html', context={'post_list': post_list})


class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=t)
