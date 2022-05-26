from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.models import Post, Comment
from blog.forms import CommentForm


class HomeView(ListView):
    model = Post
    paginate_by = 9
    template_name = 'blog/home.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = Post.objects.select_related(
                'category', 'author'
            ).filter(
                Q(title__icontains=query)
                | Q(text__icontains=query)
                | Q(category__name__icontains=query)
            )
        else:
            object_list = Post.objects.select_related(
                'category', 'author'
            ).all()
        return object_list


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(
            category__slug=self.kwargs.get("slug")
        ).select_related('category', 'author')


class PostDetailView(DetailView):
    context_object_name = "post"
    slug_url_kwarg = "post_slug"

    def get_queryset(self):
        return Post.objects.filter(
            category__slug=self.kwargs.get("slug"),
            slug=self.kwargs.get("post_slug")
        ).select_related('category', 'author').prefetch_related('recipe')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class CreateComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        form.instance.email = self.request.user.email
        form.instance.name = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()
