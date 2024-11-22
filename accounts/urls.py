from django.urls import path
from .views import UserRegistrationView, UserProfileView, UserDeleteView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/delete/', UserDeleteView.as_view(), name='delete_account'),
] 