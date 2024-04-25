# todos/views.py

from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Todo
from .serializers import TodoSerializer
from .tasks import send_notification_email

class TodoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    pagination_class = PageNumberPagination  # Add this line to enable pagination

class TodoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

def mark_todo_completed(request, todo_id):
    # Logic to mark the todo as completed
    # For example, assuming you have a Todo model with a completed field:
    todo = Todo.objects.get(id=todo_id)
    todo.completed = True
    todo.save()

    # Call the Celery task with the todo_id
    send_notification_email.delay(todo_id)

    return HttpResponse("Todo marked as completed and notification sent.")

def todo_list_viewpage(request):
    # Get all todo items
    queryset = Todo.objects.all()

    # Search query parameter
    search_query = request.GET.get('search')

    # Filter queryset based on search query
    if search_query:
        queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    # Paginate the queryset
    paginator = Paginator(queryset, 10)  # 10 items per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        page_obj = paginator.page(paginator.num_pages)

    # Render the HTML template with paginated todo items
    return render(request, 'todo_list.html', {'page_obj': page_obj})
