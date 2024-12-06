from django.db import connection
from django.test import TestCase
from django.contrib.auth.models import User
from devsearchey.models import JobPost, Profile
from django.core.management import call_command
from devsearchey.models import ForumPost
from django.utils import timezone
from datetime import timedelta
from devsearchey.models import Comment
from django.db import transaction
from django.contrib.auth import get_user_model


class ProfileModelTest(TestCase):

    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.get(user=self.user)

    def test_profile_creation(self):
        
        self.assertIsInstance(self.profile, Profile)
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.bio, 'no bio...')

    def test_profile_update(self):
        
        self.profile.bio = 'Updated bio'
        self.profile.github = 'https://github.com/testuser'
        self.profile.website = 'https://testuser.com'
        self.profile.save()

        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.bio, 'Updated bio')
        self.assertEqual(updated_profile.github, 'https://github.com/testuser')
        self.assertEqual(updated_profile.website, 'https://testuser.com')

    def test_profile_str(self):
        
        self.assertEqual(str(self.profile), 'testuser')

    def test_profile_signal_create(self):
        
        new_user = User.objects.create_user(username='newuser', password='newpassword')
        new_profile = Profile.objects.get(user=new_user)
        self.assertIsInstance(new_profile, Profile)
        self.assertEqual(new_profile.user.username, 'newuser')

    def test_profile_signal_save(self):
        
        self.user.first_name = 'Updated'
        self.user.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.user.first_name, 'Updated')

class ForumPostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.forum_post = ForumPost.objects.create(
            user=self.user,
            title='Test Forum Post',
            content='This is a test forum post content',
            category='dev_problems'
        )

    def test_forum_post_creation(self):
        
        self.assertIsInstance(self.forum_post, ForumPost)
        self.assertEqual(self.forum_post.user.username, 'testuser')
        self.assertEqual(self.forum_post.title, 'Test Forum Post')
        self.assertEqual(self.forum_post.content, 'This is a test forum post content')
        self.assertEqual(self.forum_post.category, 'dev_problems')

    def test_forum_post_update(self):
        
        self.forum_post.title = 'Updated Forum Post'
        self.forum_post.content = 'This is an updated forum post content'
        self.forum_post.save()

        updated_forum_post = ForumPost.objects.get(id=self.forum_post.id)
        self.assertEqual(updated_forum_post.title, 'Updated Forum Post')
        self.assertEqual(updated_forum_post.content, 'This is an updated forum post content')

    def test_forum_post_should_expire(self):
       
        sneaky_user = User.objects.create_user(username='SneakyUser', password='password')
        sneaky_post = ForumPost.objects.create(
            user=sneaky_user,
            title='Sneaky Post',
            content='This is a sneaky post content',
            category='dev_problems'
        )
        sneaky_post.created_at = timezone.now() - timedelta(minutes=2)
        sneaky_post.save()

        self.assertTrue(sneaky_post.should_expire())

    def test_forum_post_str(self):
        
        self.assertEqual(str(self.forum_post), 'Test Forum Post')

    def test_forum_post_likes_increment(self):
        
        initial_likes = self.forum_post.like_count
        self.forum_post.likes.add(self.user)
        self.forum_post.like_count = self.forum_post.likes.count()
        self.forum_post.save()

        updated_forum_post = ForumPost.objects.get(id=self.forum_post.id)
        self.assertEqual(updated_forum_post.like_count, initial_likes + 1)

    def test_forum_post_comments_increment(self):
        
        initial_comments = self.forum_post.comment_count
        Comment.objects.create(
            user=self.user,
            forum_post=self.forum_post,
            content='This is a test comment'
        )
        self.forum_post.comment_count = self.forum_post.comments.count()
        self.forum_post.save()

        updated_forum_post = ForumPost.objects.get(id=self.forum_post.id)
        self.assertEqual(updated_forum_post.comment_count, initial_comments + 1)

class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.forum_post = ForumPost.objects.create(
            user=self.user,
            title='Test Forum Post',
            content='This is a test forum post content',
            category='dev_problems'
        )
        self.comment = Comment.objects.create(
            user=self.user,
            forum_post=self.forum_post,
            content='This is a test comment'
        )

    def test_comment_creation(self):
        
        self.assertIsInstance(self.comment, Comment)
        self.assertEqual(self.comment.user.username, 'testuser')
        self.assertEqual(self.comment.forum_post.title, 'Test Forum Post')
        self.assertEqual(self.comment.content, 'This is a test comment')

    def test_comment_update(self):
        
        self.comment.content = 'This is an updated test comment'
        self.comment.save()

        updated_comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(updated_comment.content, 'This is an updated test comment')

    def test_comment_str(self):
        
        self.assertEqual(str(self.comment), f"Comment by {self.user.username} on {self.forum_post.title}")

    def test_comment_likes_increment(self):
        
        initial_likes = self.comment.likes.count()
        self.comment.likes.add(self.user)
        self.comment.save()

        updated_comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(updated_comment.likes.count(), initial_likes + 1)




User = get_user_model()

class JobPostModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_job_post_creation(self):
        post = JobPost.objects.create(
            user=self.user,
            post_type=JobPost.JOB_SEEKING,
            title="Software Developer",
            description="Looking for a software developer role"
        )
        self.assertEqual(post.user.username, 'testuser')
        self.assertEqual(post.post_type, JobPost.JOB_SEEKING)
        self.assertEqual(post.title, "Software Developer")
        self.assertEqual(post.description, "Looking for a software developer role")
        self.assertEqual(post.views, 0)
        self.assertEqual(post.bookmark_count, 0)

    def test_reference_number_for_job_offering(self):
        post = JobPost.objects.create(
            user=self.user,
            post_type=JobPost.JOB_OFFERING,
            title="Software Developer Job",
            description="Offering a software developer job"
        )
        post.save()
        self.assertTrue(post.reference_number.startswith('REF'))

    def test_post_str_representation(self):
        post = JobPost.objects.create(
            user=self.user,
            post_type=JobPost.JOB_SEEKING,
            title="Data Scientist",
            description="Looking for a data scientist role"
        )
        self.assertEqual(str(post), f"{self.user.username} - Data Scientist")

    def test_job_post_updated_at_changes(self):
        post = JobPost.objects.create(
            user=self.user,
            post_type=JobPost.JOB_SEEKING,
            title="Frontend Developer",
            description="Looking for a frontend developer role"
        )
        old_updated_at = post.updated_at
        post.title = "Senior Frontend Developer"
        post.save()
        self.assertNotEqual(post.updated_at, old_updated_at)
