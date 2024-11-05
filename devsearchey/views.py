from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from devsearchey.forms import UserLoginForm, UserRegistrationForm, ProfileForm, JobPostForm
from devsearchey.models import JobPost, Profile


def home_view(request):
    job_posts = JobPost.objects.all().order_by('-created_at')
    context = {'job_posts': job_posts}
    return render(request, 'home.html', context)




def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
        return render(request, 'login.html', {'form': form})
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        if 'delete_profile' in request.POST:
            request.user.delete()
            return redirect('home')
        else:
            form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid():
                form.save()
                return redirect('home')
    else:
        form = ProfileForm(instance=request.user.profile)
    avatar_url = request.user.profile.avatar.url if request.user.profile.avatar else ''
    return render(request, 'profile.html', {'form': form, 'avatar_url': avatar_url})

@login_required
def create_job_post_view(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.user = request.user
            job_post.save()
            return redirect('home')
    else:
        form = JobPostForm()
    return render(request, 'create_job_post.html', {'form': form})

@login_required
def job_post_detail_view(request, post_id):
    post = get_object_or_404(JobPost, id=post_id)
    post.views += 1
    post.save()
    return render(request, 'job_post_detail.html', {'post': post})

@login_required
def delete_job_post_view(request, post_id):
    post = get_object_or_404(JobPost, id=post_id)
    if request.method == 'POST' and post.user == request.user:
        post.delete()
        return redirect('profile')
    return redirect('profile')

@login_required
def manage_job_posts_view(request):
    job_posts = JobPost.objects.filter(user=request.user)
    return render(request, 'manage_job_posts.html', {'job_posts': job_posts})


@login_required
def bookmark_post_view(request, post_id):
    post = get_object_or_404(JobPost, id=post_id)
    profile = request.user.profile

    if post in profile.bookmarked_posts.all():
        profile.bookmarked_posts.remove(post)
        action = 'removed'
    else:
        profile.bookmarked_posts.add(post)
        action = 'added'

    post.bookmark_count = post.bookmarked_by.count()
    post.save()

    return JsonResponse({'action': action, 'bookmark_count': post.bookmark_count})

@login_required
def get_bookmarks_view(request):
    bookmarks = request.user.profile.bookmarked_posts.all()
    bookmarks_data = [{'id': post.id, 'title': post.title} for post in bookmarks]
    return JsonResponse({'bookmarks': bookmarks_data})




