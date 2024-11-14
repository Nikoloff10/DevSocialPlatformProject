from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from devsearchey.forms import CommentForm, ForumPostForm, UserLoginForm, UserRegistrationForm, ProfileForm, JobPostForm
from devsearchey.models import Comment, JobPost, Profile, ForumPost
from django.db.models import Q

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
    forum_posts = ForumPost.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'form': form, 'avatar_url': avatar_url, 'forum_posts': forum_posts})

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


@login_required
def user_forum_posts_view(request):
    forum_posts = ForumPost.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_forum_posts.html', {'forum_posts': forum_posts})

@login_required
def edit_forum_post_view(request, post_id):
    forum_post = get_object_or_404(ForumPost, id=post_id, user=request.user)
    if request.method == 'POST':
        form = ForumPostForm(request.POST, instance=forum_post)
        if form.is_valid():
            form.save()
            return redirect('user_forum_posts')
    else:
        form = ForumPostForm(instance=forum_post)
    return render(request, 'edit_forum_post.html', {'form': form})

@login_required
def delete_forum_post_view(request, post_id):
    forum_post = get_object_or_404(ForumPost, id=post_id, user=request.user)
    if request.method == 'POST':
        forum_post.delete()
        return redirect('user_forum_posts')
    return render(request, 'confirm_delete_forum_post.html', {'forum_post': forum_post})


def dev_problems_forum_view(request):
    forum_posts = ForumPost.objects.filter(category='dev_problems').order_by('-created_at')
    return render(request, 'dev_problems_forum.html', {'forum_posts': forum_posts})

def techy_nerds_forum_view(request):
    forum_posts = ForumPost.objects.filter(category='techy_nerds').order_by('-created_at')
    return render(request, 'techy_nerds_forum.html', {'forum_posts': forum_posts})

def search_view(request):
    query = request.GET.get('q')
    if query:
        
        job_post = JobPost.objects.filter(reference_number=query).first()
        if job_post:
            return redirect('job_post_detail', post_id=job_post.id)
        
        
        profiles = Profile.objects.filter(Q(user__username__icontains=query) | Q(user__email__icontains=query))
        job_posts = JobPost.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        return render(request, 'search_results.html', {'profiles': profiles, 'job_posts': job_posts})
    return render(request, 'search_results.html', {'profiles': [], 'job_posts': []})

def forum_post_detail_view(request, post_id):
    forum_post = get_object_or_404(ForumPost, id=post_id)
    comments = forum_post.comments.all().order_by('created_at')
    return render(request, 'forum_post_detail.html', {'forum_post': forum_post, 'comments': comments})

def create_forum_post_view(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            forum_post = form.save(commit=False)
            if request.user.is_authenticated:
                forum_post.user = request.user
            else:
                sneaky_user = User.objects.get(username='SneakyUser')
                forum_post.user = sneaky_user
            forum_post.category = request.POST.get('category', 'dev_problems')
            forum_post.save()
            return redirect('dev_problems_forum' if forum_post.category == 'dev_problems' else 'techy_nerds_forum')
    else:
        form = ForumPostForm()
    return render(request, 'create_forum_post.html', {'form': form})

def create_comment_view(request, post_id):
    forum_post = get_object_or_404(ForumPost, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:
                comment.user = request.user
            else:
                sneaky_user = User.objects.get(username='SneakyUser')
                comment.user = sneaky_user
            comment.forum_post = forum_post
            comment.save()
            forum_post.comment_count = forum_post.comments.count()
            forum_post.save()
            return redirect('forum_post_detail', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'create_comment.html', {'form': form})

def like_forum_post_view(request, post_id):
    forum_post = get_object_or_404(ForumPost, id=post_id)
    session_key = f'liked_{post_id}'
    
    if request.user.is_authenticated:
        if request.user in forum_post.likes.all():
            forum_post.likes.remove(request.user)
        else:
            forum_post.likes.add(request.user)
    else:
        if request.session.get(session_key):
            forum_post.like_count -= 1
            request.session[session_key] = False
        else:
            forum_post.like_count += 1
            request.session[session_key] = True
    
    forum_post.like_count = forum_post.likes.count() + sum(1 for key, value in request.session.items() if key == session_key and value)
    forum_post.save()
    return JsonResponse({'like_count': forum_post.like_count})

def like_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    comment.forum_post.like_count = comment.forum_post.comments.aggregate(total_likes=Sum('likes')).get('total_likes', 0)
    comment.forum_post.save()
    return JsonResponse({'likes_count': comment.likes.count()})