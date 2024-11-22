from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
] 