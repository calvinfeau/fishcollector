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
  path('fish/<int:fish_id>/assoc_decor/<int:decor_id>/', views.assoc_decor, name='assoc_decor'),
  path('fish/<int:fish_id>/remove_decor/<int:decor_id>/', views.remove_decor, name='remove_decor'),
  path('decors/', views.DecorList.as_view(), name='decors_index'),
  path('decors/<int:pk>/', views.DecorDetail.as_view(), name='decors_detail'),
  path('decors/create/', views.DecorCreate.as_view(), name='decors_create'),
  path('decors/<int:pk>/update/', views.DecorUpdate.as_view(), name='decors_update'),
  path('decors/<int:pk>/delete/', views.DecorDelete.as_view(), name='decors_delete'),
]

