from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Relationship

class FollowToggleView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        relationship, created = Relationship.objects.get_or_create(
            follower=request.user,
            following_id=user_id
        )
        if not created:
            relationship.delete()
            is_following = False
        else:
            is_following = True
        return JsonResponse({'is_following': is_following}) 