from django.urls import path, include

from main import views

urlpatterns = [
    path('posters/', views.postersList.as_view()),
    path('new/', views.newPostView),
    path('teams/', views.teamsList.as_view()),
    #path('products/search/', views.search),
    #path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    #path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
]