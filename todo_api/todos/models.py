from django.db import models
from .tasks import send_notification_email

class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_as_completed(self):
        self.completed = True
        self.save()

        # Call the Celery task with the todo_id
        send_notification_email.delay(self.id)
