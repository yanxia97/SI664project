from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('artwork/', views.ArtWorkListView.as_view(), name='artwork'),
    path('artwork/<int:pk>/', views.ArtWorkDetailView.as_view(), name='artwork_detail'),
]