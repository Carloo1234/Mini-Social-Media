from django.shortcuts import render
from .models import Post, Like, Comment
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, "social/index.html")

def feed(request):
    posts = Post.objects.all()
    likes = request.user.likes.values_list('post_id', flat=True)
    return render(request, "social/feed.html", {'posts': posts,
                                                'likes': likes})
@login_required
def toggle_like(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST required."}, status=400)
    post = Post.objects.get(pk=post_id)
    user = request.user
    like, created = Like.objects.get_or_create(post=post, user=user)
    if not created:
        liked = False
        like.delete()
    else:
        liked = True
    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })
    
def load_comments(request, post_id):
    comments = Comment
    return render(request, "social/comments.html", {'comments': comments})