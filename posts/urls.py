from django.urls import path
from .views import (
    PostCreateView, PostDetailView, PostDeleteView, 
    FeedView, HashtagView, HashtagPostsView, ExploreView, add_comment
)

app_name = 'posts'

urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('explore/', ExploreView.as_view(), name='explore'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('hashtag/<str:hashtag>/', HashtagView.as_view(), name='hashtag'),
    path('hashtag/<str:hashtag>/posts/', HashtagPostsView.as_view(), name='hashtag_posts'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
] 