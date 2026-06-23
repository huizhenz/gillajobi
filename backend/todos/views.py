from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Todo
from .serializers import TodoSerializer, TodoCompleteSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def todo_list(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def todo_detail(request, todo_pk):
    todo = Todo.objects.get(pk=todo_pk)

    if request.method == 'PUT':
        serializer = TodoCompleteSerializer(todo, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    elif request.method == 'DELETE':
        todo.delete()
        message = {
            'delete' : f'투두가 삭제되었습니다.'
        }
        return Response(message, status=status.HTTP_200_OK)
