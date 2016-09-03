from django.contrib.auth.models import User
from django.test import TestCase
from django.db.utils import IntegrityError
from django.utils import timezone

from ..models import BlogPost


class BehaviorTestCaseMixin(object):
    def setUp(self):
        self.user = User.objects.create_user(
            username='john',
            email='jlennon@beatles.com',
            password='glass onion'
        )

    def get_model(self):
        return getattr(self, 'model')

    def create_instance(self, **kwargs):
        raise NotImplementedError("Implement me")


class PublishableTests(BehaviorTestCaseMixin):
    def test_published(self):
        obj = self.create_instance(
            author=self.user,
            publish_date=timezone.now()
        )
        self.assertTrue(obj.is_published)
        self.assertIn(obj, self.model.objects.published())

    def test_unpublished(self):
        obj = self.create_instance(
            author=self.user,
            publish_date=None
        )
        self.assertFalse(obj.is_published)
        self.assertNotIn(obj, self.model.objects.published())


class AuthorableTest(BehaviorTestCaseMixin):
    def test_add_author_should_save(self):
        obj = self.create_instance(
            author=self.user
        )
        self.assertEqual(BlogPost.objects.all()[0], obj)

    def test_not_add_author_shoudl_railse_error(self):
        with self.assertRaises(IntegrityError):
            self.create_instance()


class BlogPostTestCase(AuthorableTest, PublishableTests, TestCase):
    model = BlogPost

    def create_instance(self, **kwargs):
        return BlogPost.objects.create(**kwargs)
