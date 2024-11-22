from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from users.models import User
from .models import Follow
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class FollowToggleView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        try:
            user_to_follow = get_object_or_404(User, id=user_id)
            
            if request.user == user_to_follow:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Vous ne pouvez pas vous suivre vous-même'
                }, status=400)

            follow, created = Follow.objects.get_or_create(
                follower=request.user,
                following=user_to_follow
            )
            
            if not created:  # Si la relation existait déjà
                follow.delete()
                is_following = False
            else:
                is_following = True

            return JsonResponse({
                'status': 'success',
                'is_following': is_following,
                'followers_count': user_to_follow.followers.count()
            })
            
        except Exception as e:
            print(f"Erreur dans FollowToggleView: {str(e)}")  # Debug
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

class FollowersListView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        followers = user.followers.select_related('follower').order_by('-created_at')
        
        followers_data = [{
            'id': follow.follower.id,
            'username': follow.follower.username,
            'profile_picture': follow.follower.profile_picture.url if follow.follower.profile_picture else None,
        } for follow in followers]
        
        return JsonResponse({'followers': followers_data})
