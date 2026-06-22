from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleDetailSerializer, CommentListSerializer, CommentDetailSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ArticleDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)
    
    elif request.method =='PUT':
        serializer = ArticleDetailSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        article.delete()
        message = {
            'delete' : f'게시글이 삭제되었습니다.'
        }
        return Response(message, status = status.HTTP_200_OK)
    

@api_view(['GET', 'POST'])
def comment_list_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)

    if request.method == 'GET':
        comments = article.comments.all()
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CommentDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['DELETE'])
def comment_delete(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == 'DELETE':
        comment.delete()
        message = {
            'delete' : f'댓글이 삭제되었습니다.'
        }
        return Response(message, status=status.HTTP_200_OK)

