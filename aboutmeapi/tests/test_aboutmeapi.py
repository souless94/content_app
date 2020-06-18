from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Content
from aboutmeapi.serializers import ContentSerializer

CONTENT_URL = reverse('content:content-list')
DOCS_URL = reverse('api-docs:docs-index')


def sample_content(author, title="Hi", description="sample Hi"):
    return Content.objects.create(
        title=title, description=description, author=author)


class PublicContentApiTests(TestCase):
    """Test the public available Content API"""

    def setUp(self):
        self.client = APIClient()
        creds = {
            'username': 'Joe',
            'password': 'pa$$word'
        }
        self.user = get_user_model().objects.create_user(**creds)
        self.content = Content.objects.create(
            title="Hello World", description="sample", author=self.user)

    def test_get_content_success(self):
        """Test that can get content"""
        res = self.client.get(CONTENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = ContentSerializer(self.content)
        self.assertIn(serializer.data, res.data)

    def test_get_content_filter_success(self):
        """Test that can get content with filter"""
        the_content = sample_content(self.user)
        params = {
            'id': self.content.id
        }
        res = self.client.get(CONTENT_URL, params)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer1 = ContentSerializer(self.content)
        serializer2 = ContentSerializer(the_content)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_not_authorised_fail(self):
        """Test that other methods are not allowed without login"""
        payload = {
            "title": 'john',
            "description": "sample description",
            "author": '1'
        }
        res = self.client.post(CONTENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.put(CONTENT_URL + "{}/".format(self.content.id), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.patch(CONTENT_URL + "{}/".format(self.content.id), payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.delete(CONTENT_URL + "{}/".format(self.content.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class DocsApiTests(TestCase):
    """Test the API documentation"""

    def setUp(self):
        self.client = APIClient()
        creds = {
            'username': 'Joe',
            'password': 'pa$$word'
        }
        self.user = get_user_model().objects.create_user(**creds)
        creds['username'] = 'john'
        self.superuser = get_user_model().objects.create_superuser(**creds)

    def test_docs_public_successful(self):
        """Test that public cannot see docs"""
        res = self.client.get(DOCS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_docs_invalid_successful(self):
        """Test that user cannot see docs"""
        self.client.force_authenticate(user=self.user)
        res = self.client.get(DOCS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_docs_valid_successful(self):
        """Test that Admin can see docs"""
        self.client.force_authenticate(user=self.superuser)
        res = self.client.get(DOCS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
