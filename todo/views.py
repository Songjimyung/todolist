from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Todolist
from .serializers import TodoSerializer, TodoCreateSerializer
from rest_framework.views import APIView

class TodoView(APIView):
    def get(self, request):
        todo = Todolist.objects.all()
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TodoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, todolist_id):
        todolist = Todolist.objects.get(id=todolist_id)
        if request.user == todolist.user:
           serializer= TodoCreateSerializer(todolist, data=request.data)
           if serializer.is_valid():
              serializer.save()
              return Response(serializer.data, status=status.HTTP_200_OK)
           else:
               return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("작성자만 수정가능합니다", status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, todolist_id):
        todolist = Todolist.objects.get(id=todolist_id)
        if request.user == todolist.user:
            todolist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("작성자만 삭제가능합니다", status=status.HTTP_403_FORBIDDEN)