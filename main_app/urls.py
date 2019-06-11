from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('fish/', views.fish_index, name="index"),
  path('fish/<int:fish_id>/', views.fish_detail, name='detail'),
  path('fish/create/', views.FishCreate.as_view(), name='fish_create'),
  path('fish/<int:pk>/update/', views.FishUpdate.as_view(), name='fish_update'),
  path('fish/<int:pk>/delete/', views.FishDelete.as_view(), name='fish_delete'),
  path('fish/<int:fish_id>/add_feeding/', views.add_feeding, name='add_feeding'),
]

