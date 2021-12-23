from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('post/<str:slug>/', PostDetailView.as_view(), name='post'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('search/', Search.as_view(), name='search'),
]

