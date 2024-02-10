from django.urls import path
from subscriptions import views

urlpatterns = [
    path('<int:owner_id>', views.SubscriptionsView.as_view()),       
]