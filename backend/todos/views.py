from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Todo
from .serializers import TodoSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def todo_list(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TodoSerializer(d)

@api_view(['DELETE'])
def todo_detail():
    pass