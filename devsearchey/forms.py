from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from devsearchey.models import Profile, JobPost, ForumPost, Comment


class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password']
        widgets = {

            'password': forms.PasswordInput()
        }

        placeholders = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'password': 'Password',
            'confirm_password': 'Confirm Password'
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user



class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400',
            'placeholder': 'Password'
        })
    )






class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded focus:outline-none focus:ring-2 focus:ring-purple-400',
            'placeholder': 'Username'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded focus:outline-none focus:ring-2 focus:ring-purple-400',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded focus:outline-none focus:ring-2 focus:ring-purple-400',
            'placeholder': 'Last Name'
        })
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded focus:outline-none focus:ring-2 focus:ring-purple-400 resize-none',
            'placeholder': 'Tell us about yourself...',
            'rows': 4
        })
    )
    github = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded focus:outline-none focus:ring-2 focus:ring-purple-400',
            'placeholder': 'GitHub Profile URL'
        })
    )
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded focus:outline-none focus:ring-2 focus:ring-purple-400',
            'placeholder': 'Personal Website URL'
        })
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded focus:outline-none focus:ring-2 focus:ring-purple-400'
        })
    )

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'bio', 'github', 'website', 'avatar']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise ValidationError('This username is already taken.')
        return username

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        user = self.user
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            profile.save()
        return profile


class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label='New Email',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded focus:outline-none focus:ring-2 focus:ring-green-500',
            'placeholder': 'New Email'
        })
    )
    confirm_email = forms.EmailField(
        required=True,
        label='Confirm New Email',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded focus:outline-none focus:ring-2 focus:ring-green-500',
            'placeholder': 'Confirm New Email'
        })
    )

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')

        if email and confirm_email and email != confirm_email:
            raise forms.ValidationError("Emails do not match.")

        if User.objects.filter(email=email).exclude(username=self.instance.username).exists():
            raise forms.ValidationError("This email is already in use.")

        return cleaned_data


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['post_type', 'title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400',
                'placeholder': 'Enter job title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'resize-none w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400',
                'rows': 4,
                'placeholder': 'Enter job description'
            }),
            'post_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400'
            }),
        }




class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'resize-none w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400',
                'rows': 4,
                'placeholder': 'Enter post content'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-600 bg-gray-700 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400 resize-none',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }
