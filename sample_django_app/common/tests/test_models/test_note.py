from django.test import TestCase

from ..test_behaviors import AuthorableTest, TimestampableTest
from ...models import Note


class NoteTest(AuthorableTest, TimestampableTest, TestCase):
    model = Note
