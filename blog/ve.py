from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post
from .forms import CommentForm


class PostDisplay(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = 'blog_list.html' ##
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        """
        Display logged in user bookings 
        paginated by 4 per page
        """
        posts = Post.objects.all()
        paginator = Paginator(Post.objects.all(), 4)
        page = request.GET.get('page')
        post_listing = paginator.get_page(page)

        return render(request, 'blog/blog_list.html',
            {
                'posts': posts,
                'post_listing': post_listing,
            })


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")

        return render(
            request,
            "blog_story",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "comment_form": CommentForm()
            },
        )
    
    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "blog_story.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
            },
        )
