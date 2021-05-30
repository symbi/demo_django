from django.urls import path

from order import views

urlpatterns = [
    path('checkout/', views.checkout),
    #path('test/', views.test),
    path('orders/', views.OrdersList.as_view()),  
]