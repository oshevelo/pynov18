from django.urls import path

from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('category/', views.CategoryList.as_view()),
    path('category/<int:pk>/', views.CategoryDetail.as_view()),
    path('manufacturer/', views.ManufacturerList.as_view()),
    path('manufacturer/<int:pk>/', views.ManufacturerDetail.as_view()),
    path('image/', views.ProductImageList.as_view()),
    path('image/<int:pk>/', views.ProductImageDetail.as_view()),
    path('', views.ProductList.as_view()),
    path('<int:pk>/', views.ProductDetail.as_view()),
]
