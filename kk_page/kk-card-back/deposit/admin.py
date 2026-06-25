from django.contrib import admin

from .models import (
    FavoriteProduct,
    FinancialOption,
    FinancialProduct,
)

admin.site.register(FinancialProduct)
admin.site.register(FinancialOption)
admin.site.register(FavoriteProduct)