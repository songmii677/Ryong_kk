from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.card_list),
    path("recommend/", views.recommend_cards),
    path("results/", views.recommend_results, name="recommend-results"),
    path("results/<int:result_pk>/", views.recommend_result_detail, name="recommend_result_detail"),
    path("<int:card_pk>/", views.card_detail),
    path('ai-recommend/', views.ai_recommend_cards)
]