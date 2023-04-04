from django.test import TestCase
from base.models import Project
from django.contrib.auth.models import User

class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.project = Project.objects.create(
            user = self.user
        )

    def test_project_creation(self):
        self.assertEqual(self.project.user, self.user)

    