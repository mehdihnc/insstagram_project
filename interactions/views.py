from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from posts.models import Post
from .models import Like, Comment
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

class LikeToggleView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        try:
            post = get_object_or_404(Post, id=post_id)
            like, created = Like.objects.get_or_create(
                user=request.user,
                post=post
            )
            
            if not created:
                like.delete()
                is_liked = False
            else:
                is_liked = True
                
            return JsonResponse({
                'status': 'success',
                'is_liked': is_liked,
                'likes_count': post.get_likes_count()
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

@login_required
@require_POST
def add_comment(request, post_id):
    try:
        # Log pour déboguer
        print("Body reçu:", request.body.decode('utf-8'))
        
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        print("Contenu:", content)
        
        if not content:
            return JsonResponse({
                'success': False,
                'error': 'Le commentaire ne peut pas être vide'
            }, status=400)
        
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            content=content
        )
        
        response_data = {
            'success': True,
            'comment': {
                'id': comment.id,
                'username': comment.user.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        
        print("Réponse:", response_data)
        return JsonResponse(response_data)
        
    except Post.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Post non trouvé'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Format de données invalide'
        }, status=400)
    except Exception as e:
        print("Erreur:", str(e))
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
@require_POST
def toggle_like(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )
        
        if not created:
            # Si le like existe déjà, on le supprime
            like.delete()
            is_liked = False
        else:
            is_liked = True
            
        likes_count = post.post_likes.count()
        
        return JsonResponse({
            'status': 'success',
            'is_liked': is_liked,
            'likes_count': likes_count
        })
        
    except Post.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Post non trouvé'
        }, status=404)
    except Exception as e:
        print(f"Erreur dans toggle_like: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400) 