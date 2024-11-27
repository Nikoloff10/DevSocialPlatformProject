from django.urls import path, include
from rest_framework.routers import DefaultRouter
from devsearchey.views import ChangeEmailView, CustomPasswordChangeView, CustomPasswordResetConfirmView, CustomPasswordResetView, DeleteProfileView, HomeView, ManageJobPostsView, ProfileDetailView, ProfileView, CreateJobPostView, JobPostDetailView, DeleteJobPostView, ForumPostDetailView, SearchView, BookmarkPostView, GetBookmarksView, DevProblemsForumView, TechyNerdsForumView, CreateForumPostView, CreateCommentView, LikeForumPostView, UserForumPostsView, EditForumPostView, DeleteForumPostView, ForumPostViewSet, CommentViewSet, JobPostViewSet, ProfileViewSet, LoginView, RegisterView, LogoutView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
router = DefaultRouter()
router.register(r'forum-posts', ForumPostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'job-posts', JobPostViewSet)
router.register(r'profiles', ProfileViewSet)

# app_name = 'devsearchey'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete-profile/', DeleteProfileView.as_view(), name='delete_profile'),
    path('create-job-post/', CreateJobPostView.as_view(), name='create_job_post'),
    path('job-post/<int:pk>/', JobPostDetailView.as_view(), name='job_post_detail'),
    path('delete-job-post/<int:pk>/', DeleteJobPostView.as_view(), name='delete_job_post'),
    path('search/', SearchView.as_view(), name='search'),
    path('bookmark-post/<int:post_id>/', BookmarkPostView.as_view(), name='bookmark_post'),
    path('get-bookmarks/', GetBookmarksView.as_view(), name='get_bookmarks'),
    path('dev-problems-forum/', DevProblemsForumView.as_view(), name='dev_problems_forum'),
    path('forum-post/<int:pk>/', ForumPostDetailView.as_view(), name='forum_post_detail'),
    path('create-forum-post/', CreateForumPostView.as_view(), name='create_forum_post'),
    path('forum-post/<int:post_id>/comment/', CreateCommentView.as_view(), name='create_comment'),
    path('forum-post/<int:post_id>/like/', LikeForumPostView.as_view(), name='like_forum_post'),
    path('techy-nerds-forum/', TechyNerdsForumView.as_view(), name='techy_nerds_forum'),
    path('user-forum-posts/', UserForumPostsView.as_view(), name='user_forum_posts'),
    path('edit-forum-post/<int:pk>/', EditForumPostView.as_view(), name='edit_forum_post'),
    path('delete-forum-post/<int:pk>/', DeleteForumPostView.as_view(), name='delete_forum_post'),
    path('manage-job-posts/', ManageJobPostsView.as_view(), name='manage_job_posts'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile_detail'),

    # Profile management urls
    path('change_password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='reset_password_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name='password_reset_complete'),

    # Change Email URL
    path('change-email/', ChangeEmailView.as_view(), name='change_email'),

    # API urls
    path('api/', include(router.urls)),
]