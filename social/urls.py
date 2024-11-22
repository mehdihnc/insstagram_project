from django.urls import path
from . import views

urlpatterns = [
    path('follow/<int:user_id>/', views.FollowToggleView.as_view(), name='follow_toggle'),
] 