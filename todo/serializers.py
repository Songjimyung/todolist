from rest_framework import serializers
from .models import Todolist

class TodoSerializer(serializers.ModelSerializer):
    
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Todolist
        fields = '__all__'

class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todolist
        fields= ['title']
