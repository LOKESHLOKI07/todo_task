from django.urls import path
from .views import TodoListCreateAPIView, TodoRetrieveUpdateDestroyAPIView, todo_list_viewpage, mark_todo_completed

urlpatterns = [
    path('', TodoListCreateAPIView.as_view(), name='todo-list-create'),
    path('todos/<int:pk>/', TodoRetrieveUpdateDestroyAPIView.as_view(), name='todo-detail'),
    path('todo_list_viewpage/', todo_list_viewpage, name='todo_list_viewpage'),
    path('todos/<int:todo_id>/mark-completed/', mark_todo_completed, name='mark-todo-completed'),
]
