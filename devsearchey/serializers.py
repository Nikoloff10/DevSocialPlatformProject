from rest_framework import serializers
from django.contrib.auth.models import User
from devsearchey.models import ForumPost, Comment, JobPost, Profile

class ForumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumPost
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'avatar_url', 'github', 'website']

    def get_avatar_url(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return 'https://res.cloudinary.com/dfxbvixpv/image/upload/v1731942244/j4spsms91wb541cu9bvh.png'