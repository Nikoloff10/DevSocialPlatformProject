from django.urls import path

from devsearchey.views import home_view, login_view, register_view, logout_view, profile_view, create_job_post_view, \
    job_post_detail_view, delete_job_post_view, manage_job_posts_view, bookmark_post_view, get_bookmarks_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
    path('logout', logout_view, name='logout'),
    path('profile', profile_view, name='profile'),
    path('create-job-post', create_job_post_view, name='create_job_post'),
    path('job-post/<int:post_id>', job_post_detail_view, name='job_post_detail'),
    path('delete-job-post/<int:post_id>', delete_job_post_view, name='delete_job_post'),
    path('manage-job-posts', manage_job_posts_view, name='manage_job_posts'),
    path('job-post/<int:post_id>/', job_post_detail_view, name='job_post_detail'),
    path('bookmark-post/<int:post_id>/', bookmark_post_view, name='bookmark_post'),
    path('get-bookmarks/', get_bookmarks_view, name='get_bookmarks'),
]