from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Post
from .forms import PostForm, SignUpForm, UserEditForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


# Create your views here. 
def home(request):
    if request.user.is_authenticated:
        form = PostForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, ("Your Post has posted"))
                return redirect('home')
        posts = Post.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"posts": posts, "form": form})
    else:
        posts = Post.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"posts": posts})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', { 'profiles': profiles})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
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
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')
    
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in"))
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
            messages.success(request, ("Thank you for registering. \n Welcome to our app"))
            return redirect('home')
    return render(request, 'register.html', {'form':form})
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        
        user_form = UserEditForm(request.POST or None, request.FILES or None,  instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            login(request, current_user)
            messages.success(request, ("Your profile has been updated"))
            return redirect('home')

        return render(request, 'update_user.html', {'user_form':user_form, 'profile_form':profile_form})
    else:
        messages.success(request, ("You Must Be logged on. \n Returning Home"))
        return redirect('home')
    
def post_like(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if post.likes.filter(id=request.user.id):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        messages.success(request, ("you Must be logged in"))
        return redirect('home')