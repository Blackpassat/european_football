from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('teams/', views.TeamListView.as_view(), name='teams'),
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('players/<int:pk>/', views.PlayerDetailView.as_view(), name='player_detail'),
    path('teams/new/', views.TeamCreateView.as_view(), name='team_new'),
    path('teams/<int:pk>/delete/', views.TeamDeleteView.as_view(), name='team_delete'),
    path('teams/<int:pk>/update/', views.TeamUpdateView.as_view(), name='team_update'),
    path('teams/filter/', views.TeamFilterView.as_view(), name='team_filter'),
]