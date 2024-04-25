from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Todo
from .serializers import TodoSerializer

class TodoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_url = reverse('todo-list-create')  # Update URL name here
        self.update_url = reverse('todo-detail', kwargs={'pk': 1})
        self.todo_data = {'title': 'Test Todo', 'description': 'Test Description', 'completed': False}
        self.todo = Todo.objects.create(title='Test Todo', description='Test Description', completed=False)

    def test_create_todo(self):
        response = self.client.post(self.create_url, self.todo_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)

    def test_update_todo(self):
        updated_data = {'title': 'Updated Todo', 'description': 'Updated Description', 'completed': True}
        response = self.client.put(self.update_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Todo.objects.get(pk=1).title, 'Updated Todo')

    def test_list_todos(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Assuming only one todo exists in the database

    def test_retrieve_todo(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Todo')

    def test_mark_todo_completed(self):
        mark_completed_url = reverse('mark-todo-completed', kwargs={'todo_id': self.todo.id})
        response = self.client.post(mark_completed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Todo.objects.get(pk=self.todo.id).completed)

    def test_create_todo_invalid_data(self):
        invalid_data = {'title': '', 'description': 'Invalid Description', 'completed': False}
        response = self.client.post(self.create_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Todo.objects.count(), 1)  # No new todo should be created

    def test_delete_todo(self):
        delete_url = reverse('todo-detail', kwargs={'pk': self.todo.id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)  # Todo should be deleted from the database
from django.test import TestCase
from django.core.mail import outbox
from .tasks import send_notification_email
from celery.contrib.testing.worker import start_worker


class CeleryTaskTestCase(TestCase):
    def setUp(self):
        # Start Celery worker for testing
        self.worker = start_worker(send_notification_email.app)

    def tearDown(self):
        # Stop Celery worker after testing
        self.worker.stop()


