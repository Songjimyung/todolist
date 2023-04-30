from django.db import models
from users.models import User


class Todolist(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completion_at = models.DateTimeField(blank=True, null=True)