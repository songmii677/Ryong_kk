from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('delete/', views.delete_account, name='delete_account'),
]