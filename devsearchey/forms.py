from django import forms
from django.contrib.auth.hashers import make_password
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
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())






class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'github', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5, 'placeholder': 'no bio...', 'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none'}),
            'avatar': forms.FileInput(attrs={'class': 'custom-file-input'}),
            'github': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none'}),
            'website': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    placeholders = {
        'bio': 'Bio',
        'avatar': 'Avatar',
        'github': 'Github',
        'website': 'Website'
    }


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['post_type', 'title', 'description']
        widgets = {
            'post_type': forms.Select(),
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Description', 'maxlength': 200}),
        }



class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']