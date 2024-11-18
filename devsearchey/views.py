from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from devsearchey.forms import CommentForm, ForumPostForm, UserLoginForm, UserRegistrationForm, ProfileForm, JobPostForm
from devsearchey.models import Comment, JobPost, Profile, ForumPost
from devsearchey.serializers import ForumPostSerializer, CommentSerializer, JobPostSerializer, ProfileSerializer
from django.db.models import Q
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView

class HomeView(ListView):
    model = JobPost
    template_name = 'home.html'
    context_object_name = 'job_posts'
    ordering = ['-created_at']

class LoginView(FormView):
    template_name = 'login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            auth_login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('home')

class ProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avatar = self.request.user.profile.avatar
        if isinstance(avatar, InMemoryUploadedFile):
            context['avatar_url'] = None 
        else:
            context['avatar_url'] = avatar.url if avatar else 'https://res.cloudinary.com/dfxbvixpv/image/upload/v1731942244/j4spsms91wb541cu9bvh.png'
        context['forum_posts'] = ForumPost.objects.filter(user=self.request.user).order_by('-created_at')
        return context

class DeleteProfileView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        user.delete()
        return redirect('home')


class CreateJobPostView(LoginRequiredMixin, CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'create_job_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class JobPostDetailView(LoginRequiredMixin, DetailView):
    model = JobPost
    template_name = 'job_post_detail.html'
    context_object_name = 'post'

    def get_object(self):
        post = super().get_object()
        post.views += 1
        post.save()
        return post

class DeleteJobPostView(LoginRequiredMixin, DeleteView):
    model = JobPost
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return JobPost.objects.filter(user=self.request.user)

class ManageJobPostsView(LoginRequiredMixin, ListView):
    model = JobPost
    template_name = 'manage_job_posts.html'
    context_object_name = 'job_posts'

    def get_queryset(self):
        return JobPost.objects.filter(user=self.request.user)

class BookmarkPostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
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

class GetBookmarksView(LoginRequiredMixin, View):
    def get(self, request):
        bookmarks = request.user.profile.bookmarked_posts.all()
        bookmarks_data = [{'id': post.id, 'title': post.title} for post in bookmarks]
        return JsonResponse({'bookmarks': bookmarks_data})

class UserForumPostsView(LoginRequiredMixin, ListView):
    model = ForumPost
    template_name = 'user_forum_posts.html'
    context_object_name = 'forum_posts'

    def get_queryset(self):
        return ForumPost.objects.filter(user=self.request.user).order_by('-created_at')

class EditForumPostView(LoginRequiredMixin, UpdateView):
    model = ForumPost
    form_class = ForumPostForm
    template_name = 'edit_forum_post.html'
    success_url = reverse_lazy('user_forum_posts')

    def get_queryset(self):
        return ForumPost.objects.filter(user=self.request.user)

class DeleteForumPostView(LoginRequiredMixin, DeleteView):
    model = ForumPost
    template_name = 'confirm_delete_forum_post.html'
    success_url = reverse_lazy('user_forum_posts')

    def get_queryset(self):
        return ForumPost.objects.filter(user=self.request.user)

class DevProblemsForumView(ListView):
    model = ForumPost
    template_name = 'dev_problems_forum.html'
    context_object_name = 'forum_posts'

    def get_queryset(self):
        return ForumPost.objects.filter(category='dev_problems').order_by('-created_at')

class TechyNerdsForumView(ListView):
    model = ForumPost
    template_name = 'techy_nerds_forum.html'
    context_object_name = 'forum_posts'

    def get_queryset(self):
        return ForumPost.objects.filter(category='techy_nerds').order_by('-created_at')

class SearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        if query:
            job_post = JobPost.objects.filter(reference_number=query).first()
            if job_post:
                return redirect('job_post_detail', pk=job_post.id)

            profiles = Profile.objects.filter(Q(user__username__icontains=query) | Q(user__email__icontains=query))
            job_posts = JobPost.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
            return render(request, 'search_results.html', {'profiles': profiles, 'job_posts': job_posts})
        return render(request, 'search_results.html', {'profiles': [], 'job_posts': []})

class ForumPostDetailView(DetailView):
    model = ForumPost
    template_name = 'forum_post_detail.html'
    context_object_name = 'forum_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('created_at')
        return context

class CreateForumPostView(LoginRequiredMixin, CreateView):
    model = ForumPost
    form_class = ForumPostForm
    template_name = 'create_forum_post.html'

    def form_valid(self, form):
        forum_post = form.save(commit=False)
        if self.request.user.is_authenticated:
            forum_post.user = self.request.user
        else:
            sneaky_user = User.objects.get(username='SneakyUser')
            forum_post.user = sneaky_user
        forum_post.category = self.request.POST.get('category', 'dev_problems')
        forum_post.save()
        return redirect('dev_problems_forum' if forum_post.category == 'dev_problems' else 'techy_nerds_forum')

class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'create_comment.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        forum_post = get_object_or_404(ForumPost, id=self.kwargs['post_id'])
        if self.request.user.is_authenticated:
            comment.user = self.request.user
        else:
            sneaky_user = User.objects.get(username='SneakyUser')
            comment.user = sneaky_user
        comment.forum_post = forum_post
        comment.save()
        forum_post.comment_count = forum_post.comments.count()
        forum_post.save()
        return redirect('forum_post_detail', post_id=self.kwargs['post_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(ForumPost, id=self.kwargs['post_id'])
        return context

class LikeForumPostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(ForumPost, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            action = 'unliked'
        else:
            post.likes.add(request.user)
            action = 'liked'
        post.like_count = post.likes.count()
        post.save()
        return JsonResponse({'action': action, 'like_count': post.like_count})

class LikeCommentView(LoginRequiredMixin, View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            action = 'unliked'
        else:
            comment.likes.add(request.user)
            action = 'liked'
        comment.like_count = comment.likes.count()
        comment.save()
        return JsonResponse({'action': action, 'like_count': comment.like_count})

class ForumPostViewSet(viewsets.ModelViewSet):
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = [IsAdminUser]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]

class JobPostViewSet(viewsets.ModelViewSet):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAdminUser]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]