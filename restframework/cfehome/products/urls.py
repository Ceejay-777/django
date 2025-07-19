from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListCreateAPIView.as_view(), name='product-create'),
    # path('list/', views.ProductListCreateAPIView.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-details'),
    path('<int:pk>/update', views.ProductUpdateAPIView.as_view(), name='product-update'),
    path('<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-details'),
]

# urlpatterns = [
#     path('', views.product_alt_view, name='product-create'),
#     # path('list/', views.ProductListCreateAPIView.as_view(), name='product-list'),
#     path('<int:pk>/', views.product_alt_view, name='product-details'),
# ]