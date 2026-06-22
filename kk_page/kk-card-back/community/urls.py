from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:article_pk>/', views.article_detail, name='article_detail'),
    path('articles/<int:article_pk>/comments/', views.comment_create, name='comment_create'),
    path('comments/<int:comment_pk>/', views.comment_detail, name='comment_detail'),
    path('articles/<int:article_pk>/like/', views.toggle_article_like, name='toggle_article_like'),
    path('comments/<int:comment_pk>/like/', views.toggle_comment_like, name='toggle_comment_like')
]