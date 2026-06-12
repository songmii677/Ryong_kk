from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.card_list),
    path("recommend/", views.recommend_cards),
    path("<int:card_pk>/", views.card_detail),
]