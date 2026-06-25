from django.urls import path

from . import views


app_name = "deposit"


urlpatterns = [
    path(
        "",
        views.financial_product_list,
        name="financial-product-list",
    ),
    path(
        "load/",
        views.load_financial_products,
        name="load-financial-products",
    ),
    path(
        "favorites/",
        views.favorite_product_list,
        name="favorite-product-list",
    ),
    path(
        "<int:product_pk>/favorite/",
        views.toggle_favorite_product,
        name="toggle-favorite-product",
    ),
    path(
        "<int:product_pk>/",
        views.financial_product_detail,
        name="financial-product-detail",
    ),
]