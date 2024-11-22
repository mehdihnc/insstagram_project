from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q, Count
from django.contrib import messages
from .models import Post, Hashtag
from .forms import PostForm
from users.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from interactions.models import Comment
from interactions.models import Like
from django.utils import timezone

# Create your views here.

class FeedView(LoginRequiredMixin, ListView):
    template_name = 'posts/feed.html'
    model = Post
    context_object_name = 'posts'
    
    def get_queryset(self):
        posts = Post.objects.select_related('user').prefetch_related(
            'post_likes',
            'post_comments',
            'hashtags'
        ).order_by('-created_at')
        
        # Préparons les données de likes pour chaque post
        for post in posts:
            post.is_liked = post.is_liked_by_user(self.request.user)
        
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create_post.html'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        print("Post créé avec caption:", form.instance.caption)
        print("Hashtags associés:", form.instance.hashtags.all())
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Erreur lors de la création du post. Veuillez réessayer.')
        return super().form_invalid(form)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['likes_count'] = post.get_likes_count()
        context['is_liked'] = post.is_liked_by_user(self.request.user)
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('feed')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({'liked': liked, 'count': post.likes.count()})

class HashtagView(LoginRequiredMixin, ListView):
    template_name = 'posts/hashtag_posts.html'
    context_object_name = 'posts'
    paginate_by = 12

    def get_queryset(self):
        hashtag = self.kwargs['hashtag']
        return Post.objects.filter(
            caption__icontains=f'#{hashtag}'
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hashtag'] = self.kwargs['hashtag']
        context['posts_count'] = self.get_queryset().count()
        return context

class HashtagPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/hashtag_posts.html'
    context_object_name = 'posts'
    paginate_by = 12

    def get_queryset(self):
        hashtag_name = self.kwargs['hashtag'].lower()
        self.hashtag = get_object_or_404(Hashtag, name=hashtag_name)
        return Post.objects.filter(
            hashtags=self.hashtag
        ).select_related('user').prefetch_related(
            'likes', 
            'comments'
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hashtag'] = self.hashtag
        return context

class ExploreView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/explore.html'
    context_object_name = 'posts'
    paginate_by = 12

    def get_queryset(self):
        posts = Post.objects.exclude(user=self.request.user).select_related(
            'user'
        ).prefetch_related(
            'post_likes',
            'post_comments'
        ).order_by('-created_at')
        
        # Ajouter l'état des likes pour chaque post
        for post in posts:
            post.is_liked = post.is_liked_by_user(self.request.user)
        
        return posts

@login_required
@require_POST
def add_comment(request, post_id):
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({
                'success': False,
                'error': 'Le commentaire ne peut pas être vide'
            }, status=400)
        
        post = get_object_or_404(Post, id=post_id)
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            content=content
        )
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'username': comment.user.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
@require_POST
def like_post(request, post_id):
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
        'success': True,
        'is_liked': is_liked,
        'likes_count': post.get_likes_count()
    })
