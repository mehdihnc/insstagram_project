from django.urls import path
from .views import (
    RegisterView, CustomLoginView, CustomLogoutView,
    UserProfileView, EditProfileView, DeleteAccountView
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/<int:pk>/delete/', DeleteAccountView.as_view(), name='delete_account'),
]