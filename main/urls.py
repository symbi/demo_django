from django.urls import path, include

from main import views

urlpatterns = [
    path('posters/', views.postersListView),
    #path('posters/<int:id>', views.posterView),
    path('vote/<int:id>/', views.voteView),
    #path('comment/<int:id>/vote', commentVoteView),


    path('new/', views.newPostView),
    path('new_comment/', views.newCommentView),
    path('teams/', views.teamsList.as_view()),

    #path('products/search/', views.search),
    #path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    #path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
]