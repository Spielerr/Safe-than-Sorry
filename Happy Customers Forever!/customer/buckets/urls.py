from django.urls import path, include
from . import views


urlpatterns = [
    # path('hotel/<str:hotelname>/', views.categories, name='cat-page-hotel'),
    path('bank/<str:bank>/', views.categories_banks, name='cat-page-banks'),
]
