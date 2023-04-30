from django.urls import path, include
from todo import views

urlpatterns = [
    path('', views.TodoView.as_view(), name='todo_view'),   
    path('<int:todolist_id>/', views.TodoView.as_view()),
]
