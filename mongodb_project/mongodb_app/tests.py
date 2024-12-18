# mongodb_app/tests.py
from django.test import Client, TestCase
from .models import Category, Document

class MongodbAppTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.document = Document.objects.create(
            title='Test Document',
            content='This is a test document.',
            category=self.category
        )

    def test_index_view(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Document')
        self.assertContains(response, 'Test Category')
