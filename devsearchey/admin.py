from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from .models import ForumPost, Comment, JobPost, Profile

class MyAdminSite(AdminSite):
    site_header = _("DevSearchey Admin")
    site_title = _("DevSearchey Admin Portal")
    index_title = _("Welcome to DevSearchey Admin")

admin_site = MyAdminSite(name='devsearcheyadmin')

class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at', 'like_count', 'comment_count')
    search_fields = ('title', 'content', 'user__username')
    list_filter = ('created_at', 'updated_at', 'user')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'forum_post', 'created_at', 'updated_at')
    search_fields = ('content', 'user__username', 'forum_post__title')
    list_filter = ('created_at', 'updated_at', 'user')

class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at', 'views', 'bookmark_count')
    search_fields = ('title', 'description', 'user__username')
    list_filter = ('created_at', 'updated_at', 'user')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'github')
    search_fields = ('user__username', 'bio', 'github')
    list_filter = ('user',)

# Register models with the custom admin site
admin_site.register(ForumPost, ForumPostAdmin)
admin_site.register(Comment, CommentAdmin)
admin_site.register(JobPost, JobPostAdmin)
admin_site.register(Profile, ProfileAdmin)