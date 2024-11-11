from django.urls import path
from devsearchey.views import create_comment_view, create_forum_post_view, delete_forum_post_view, edit_forum_post_view, forum_post_detail_view, home_view, like_forum_post_view, login_view, register_view, logout_view, profile_view, create_job_post_view, \
    job_post_detail_view, delete_job_post_view, manage_job_posts_view, bookmark_post_view, get_bookmarks_view, \
    dev_problems_forum_view, techy_nerds_forum_view, search_view, user_forum_posts_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile', profile_view, name='profile'),
    path('create-job-post', create_job_post_view, name='create_job_post'),
    path('job-post/<int:post_id>', job_post_detail_view, name='job_post_detail'),
    path('delete-job-post/<int:post_id>', delete_job_post_view, name='delete_job_post'),
    path('manage-job-posts', manage_job_posts_view, name='manage_job_posts'),
    path('bookmark-post/<int:post_id>/', bookmark_post_view, name='bookmark_post'),
    path('get-bookmarks/', get_bookmarks_view, name='get_bookmarks'),
    path('dev-problems-forum/', dev_problems_forum_view, name='dev_problems_forum'),
    path('forum-post/<int:post_id>/', forum_post_detail_view, name='forum_post_detail'),
    path('create-forum-post/', create_forum_post_view, name='create_forum_post'),
    path('forum-post/<int:post_id>/comment/', create_comment_view, name='create_comment'),
    path('forum-post/<int:post_id>/like/', like_forum_post_view, name='like_forum_post'),
    path('techy-nerds-forum/', techy_nerds_forum_view, name='techy_nerds_forum'),
    path('search/', search_view, name='search'),
    path('user-forum-posts/', user_forum_posts_view, name='user_forum_posts'),
    path('edit-forum-post/<int:post_id>/', edit_forum_post_view, name='edit_forum_post'),
    path('delete-forum-post/<int:post_id>/', delete_forum_post_view, name='delete_forum_post'),
]