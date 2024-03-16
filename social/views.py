from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Post, Comment
from .forms import PostForm, SignUpForm, UserEditForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Post, Comment
from .forms import PostForm, SignUpForm, UserEditForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import permission_required, login_required


# Create your views here.
@login_required(login_url="/login/")
def home(request):
    show_comment = True
    form = PostForm(request.POST or None,  request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, ("Your Post has posted"))
            return redirect('home') 
    posts = Post.objects.all().order_by("-created_at")
    return render(request, 'home.html', {"posts": posts, "form": form, "show_comment": show_comment})
    

@permission_required("profile_list", login_url="/login/")
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'profile_list.html', { 'profiles': profiles})
    
@permission_required("profile", login_url="/login/")    
def profile(request, pk):
    profile = Profile.objects.get(user_id=pk)
    posts = Post.objects.filter(user_id=pk).order_by("-created_at")
    #post form logic
    if request.method=="POST":
        # Get current user 
        current_user_profile = request.user.profile
        # Get Form Data
        action = request.POST['follow']
        # Decide to follow or unfollow
        if action == "unfollow":
            current_user_profile.follows.remove(profile)
        elif action == "follow":
            current_user_profile.follows.add(profile)
            # Save the profile
        current_user_profile.save()
    return render(request, "profile.html", {"profile":profile, "posts":posts })
    
    
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Welcome Back!! \n enJoy"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, please try again"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out, please come again"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            # Login User
            user =  authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Thank you for registering. \n Welcome to our app \n let's share some Joy \n enJoy"))
            return redirect('home')
    return render(request, 'register.html', {'form':form})

@permission_required("update_user", login_url="/login/")    
def update_user(request):
    current_user = User.objects.get(id=request.user.id)
    profile_user = Profile.objects.get(user__id=request.user.id)
    
    user_form = UserEditForm(request.POST or None, request.FILES or None,  instance=current_user)
    profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        
        login(request, current_user)
        messages.success(request, ("Your profile has been updated"))
        return redirect('profile', pk=request.user.id)

    return render(request, 'update_user.html', {'user_form':user_form, 'profile_form':profile_form})
    
@permission_required("post_like", login_url="/login/")
def post_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.likes.filter(id=request.user.id):
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

@permission_required("post_show", login_url="/login/")
def post_show(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post:
        return render(request, 'show_post.html', {'post':post})
    else:
        messages.success(request, ("That post does not exist"))
        return redirect('home')
        
@permission_required("post_delete", login_url="/login/")            
def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    # Check to see if it is your post
    if request.user.username == post.user.username:
        # Delete the Post
        post.delete()
        messages.success(request, ("The post has been deleted"))
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, ("That's not your post"))
        return redirect('home')
    
@permission_required("post_edit", login_url="/login/")    
def post_edit(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user.username == post.user.username:
        form = PostForm(request.POST or None,  request.FILES or None, instance=post)
        if request.method == "POST":
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, ("Your Post has been updated"))
                return redirect('home')
        else:
            return render(request, 'edit_post.html', {'form':form, 'post':post})        
    else:
        messages.success(request, ("That's not your post"))
        return redirect('home')

@permission_required("comment", login_url="/login/")
def comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    # A Form for a Comment Model
    if request.method == 'POST':
        comment = request.POST['comment']
        post.comments.create(user=request.user, body=comment, date_added=timezone.now())
        messages.success(request, f'Comment added successfully!')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
@permission_required("comment_delete", login_url="/login/")
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    # Check to see if it is your comment
    if request.user.username == comment.user.username:
        # Delete the Comment
        comment.delete()
        messages.success(request, ("The comment has been deleted"))
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, ("That's not your comment"))
        return redirect('home')
