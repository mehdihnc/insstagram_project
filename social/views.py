from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from users.models import User
from .models import Follow
from django.views.generic import ListView

# Create your views here.

class FollowToggleView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        
        if request.user == user_to_follow:
            return JsonResponse({'error': 'Vous ne pouvez pas vous suivre vous-même'}, status=400)
            
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        
        if not created:
            follow.delete()
            is_following = False
        else:
            is_following = True
            
        return JsonResponse({
            'is_following': is_following,
            'followers_count': user_to_follow.followers.count()
        })

class FollowersListView(LoginRequiredMixin, ListView):
    template_name = 'social/followers_list.html'
    context_object_name = 'followers'
    
    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        return user.followers.all()

class FollowingListView(LoginRequiredMixin, ListView):
    template_name = 'social/following_list.html'
    context_object_name = 'following'
    
    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        return user.following.all()
