from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
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

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('devsearchey.change_jobpost') or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('devsearchey.delete_jobpost') or request.user.is_superuser


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'github')
    search_fields = ('user__username', 'bio', 'github')
    list_filter = ('user',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm('devsearchey.change_profile') and not request.user.is_superuser:
            for field in form.base_fields:
                form.base_fields[field].disabled = True
        return form
    
    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('devsearchey.change_profile') or request.user.is_superuser



admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

admin_site.register(ForumPost, ForumPostAdmin)
admin_site.register(Comment, CommentAdmin)
admin_site.register(JobPost, JobPostAdmin)
admin_site.register(Profile, ProfileAdmin)