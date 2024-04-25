from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_notification_email(todo_id):
    # Fetch the todo object using todo_id
    from .models import Todo
    todo = Todo.objects.get(id=todo_id)

    # Send email notification
    subject = 'Todo Completed'
    message = f'Todo "{todo.title}" has been marked as completed.'
    recipient_list = ['']  # Replace with your email address
    send_mail(subject, message, 'dhonilokesh7@gmail.com', recipient_list)


