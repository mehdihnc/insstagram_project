from django.urls import path
from . import views

app_name = 'follows'

urlpatterns = [
    path('toggle/<int:user_id>/', views.FollowToggleView.as_view(), name='toggle'),
] 