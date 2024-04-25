import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_api.settings')
django.setup()

from .models import Todo
import logging

logger = logging.getLogger(__name__)


def delete_completed_todos():
    try:
        # Get completed todos
        completed_todos = Todo.objects.filter(completed=True)

        # Log the number of completed todos
        logger.info(f"Number of completed todos to delete: {completed_todos.count()}")

        # Delete completed todos
        completed_todos.delete()

        logger.info("Completed todos deleted successfully.")
    except Exception as e:
        logger.exception("An error occurred while deleting completed todos.")
