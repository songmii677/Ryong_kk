from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from django.shortcuts import get_object_or_404

## 게시글 
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all().order_by('-created_at')
        serializer = ArticleSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'GET':
        serializer = ArticleSerializer(article, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user != article.user:
            return Response(
                {'error': '권한 없음'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ArticleSerializer(article, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.user != article.user:
            return Response(
                {'error': '권한 없음'},
                status=status.HTTP_403_FORBIDDEN
            )

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

## 내가 작성한 글 + 댓글
@api_view(['GET'])
def my_community(request):

    my_articles = Article.objects.filter(
        user=request.user
    )

    my_comments = Comment.objects.filter(
        user=request.user
    )

    article_data = ArticleSerializer(
        my_articles,
        many=True,
        context={'request': request}
    ).data

    comment_data = []

    for comment in my_comments:
        comment_data.append({
            'id': comment.id,
            'content': comment.content,
            'article_id': comment.article.id,
            'article_title': comment.article.title
        })

    return Response({
        'articles': article_data,
        'comments': comment_data
    })

## 좋아요
@api_view(['POST'])
def toggle_article_like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.user in article.likes.all():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True

    return Response({
        "liked": liked,
        "like_count": article.likes.count()
    })

## 댓글
@api_view(['POST'])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save(user=request.user, article=article)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

## 수정, 삭제
@api_view(['PUT', 'DELETE'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user != comment.user:
        return Response(
            {'error':'권한 없음'},
            status=status.HTTP_403_FORBIDDEN
        )
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=comment.user, article=comment.article)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

## 좋아요
@api_view(['POST'])
def toggle_comment_like(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True

    return Response({
        "liked": liked,
        "like_count": comment.likes.count()
    })