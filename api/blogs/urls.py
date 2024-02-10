from django.urls import path
from blogs import views

urlpatterns = [
    path('feed', views.FeedView.as_view()),
    path('posts', views.BlogsPostView.as_view()),
    path('posts/<int:post_id>', views.BlogPostDeleteView.as_view()), 
    path('posts/<int:post_id>/read', views.BlogPostReadView.as_view()),       
]