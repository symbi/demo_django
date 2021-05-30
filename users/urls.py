from django.urls import path, include

from users.views import signUpView

urlpatterns = [
    path('signup/', signUpView, name = 'signup'),
    #path('tests/', views.testsList.as_view()),
    #path('products/search/', views.search),
    #path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    #path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
]