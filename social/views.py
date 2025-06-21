from django.shortcuts import render
from .models import Post, Like, Comment
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class LoginForm(AuthenticationForm):
    # full_name = forms.CharField(max_length=100)
    # email = forms.EmailField()
    # password = forms.PasswordInput
    pass

class UserCreationFormExtended(UserCreationForm):
    full_name = forms.CharField(required=True, label="Full Name")
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "password1", "password2")
    

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("feed"))
    else:
        return HttpResponseRedirect(reverse("signup_view"))


@login_required
def feed(request):
    if request.method == 'POST':
        post_id = request.POST.get("post_id")
        delete_post(request, post_id)
        return HttpResponseRedirect(reverse("feed"))
    posts = Post.objects.all().order_by('-id')
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

@login_required
def load_comments(request, post_id):
    if request.method == 'POST':
        if request.POST.get("action") == "add":
            add_comment(request, post_id)
        else:
            comment_id = request.POST.get("comment_id")
            delete_comment(request, comment_id)
        return HttpResponseRedirect(reverse("load_comments", args=(post_id,)))
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post).all()
    return render(request, "social/comments.html", {'post': post,
                                                    'comments': comments})
@login_required  
def add_comment(request, post_id):
    content = request.POST.get("content")
    Comment.objects.create(user=request.user, post=Post.objects.get(pk=post_id), content=content)

@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    
@login_required
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    
    
@login_required
def add_post(request):
    if request.method == 'POST':
        content = request.POST.get("content")
        Post.objects.create(user=request.user, content=content)
        return HttpResponseRedirect(reverse("feed"))
    return render(request, "social/add_post.html")

def signup_view(request):
    form = UserCreationFormExtended(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.full_name = form.cleaned_data["full_name"]
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("feed"))
    return render(request, "social/signup.html", {"form": form})

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse("feed"))

    return render(request, "social/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))