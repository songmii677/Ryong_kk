from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer

@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, article_pk):

    article = Article.objects.get(pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':

        if request.user != article.user:
            return Response(
                {'error': '권한 없음'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ArticleSerializer(
            article,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':

        if request.user != article.user:
            return Response(
                {'error': '권한 없음'},
                status=status.HTTP_403_FORBIDDEN
            )

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
## 댓글
@api_view(['POST'])
def comment_create(request, article_pk):

    article = Article.objects.get(pk=article_pk)

    serializer = CommentSerializer(
        data=request.data
    )

    if serializer.is_valid():
        serializer.save(
            user=request.user,
            article=article
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
@api_view(['PUT', 'DELETE'])
def comment_detail(request, comment_pk):

    comment = Comment.objects.get(
        pk=comment_pk
    )

    if request.user != comment.user:
        return Response(
            {'error':'권한 없음'},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'PUT':

        serializer = CommentSerializer(
            comment,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data
            )

    elif request.method == 'DELETE':

        comment.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )