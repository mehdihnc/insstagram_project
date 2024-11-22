from django.urls import path, include

urlpatterns = [
    path('', include('posts.urls')),
    path('accounts/', include('accounts.urls')),
    path('interactions/', include('interactions.urls')),
] 