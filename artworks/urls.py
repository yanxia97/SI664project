from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('artwork/', views.ArtWorkListView.as_view(), name='artwork'),
    path('artwork/<int:pk>/', views.ArtWorkDetailView.as_view(), name='artwork_detail'),
    path('artist/', views.ArtistListView.as_view(), name='artist'),
    path('artist/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),
]