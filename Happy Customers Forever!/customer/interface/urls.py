from django.urls import path, include
from . import views

urlpatterns = [
    path('banks/', views.banks, name='banks-int')
    # path('inter/', views.interface, name='interface-page'),
]
