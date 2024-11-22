from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from posts.models import Post
from .models import User, Profile
from .forms import UserRegistrationForm, UserUpdateForm, UserLoginForm, UserProfileForm, CombinedProfileForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.views import View
from interactions.models import Like, Comment
from follows.models import Follow

# Create your views here.

class RegisterView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('posts:feed')

class CustomLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        response = redirect('users:login')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

class UserProfileView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        # Créer un profil s'il n'existe pas
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)
        
        # Stats
        context['stats'] = {
            'posts_count': Post.objects.filter(user=user).count(),
            'followers_count': user.followers.count(),
            'following_count': user.following.count()
        }
        
        # Posts avec préchargement
        context['posts'] = Post.objects.filter(user=user).prefetch_related(
            'post_likes', 'post_comments'
        ).order_by('-created_at')
        
        # Activité récente
        context['recent_likes'] = Like.objects.filter(user=user).select_related(
            'post', 'post__user'
        ).order_by('-created_at')[:5]
        
        context['recent_comments'] = Comment.objects.filter(user=user).select_related(
            'post', 'post__user'
        ).order_by('-created_at')[:5]
        
        # Vérifier si l'utilisateur connecté suit ce profil
        if self.request.user.is_authenticated and self.request.user != user:
            context['is_following'] = Follow.objects.filter(
                follower=self.request.user,
                following=user
            ).exists()
        
        # Debug pour vérifier l'avatar
        print("Avatar URL:", user.profile.avatar.url if user.profile.avatar else "No avatar")
        
        return context

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/edit_profile.html'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.object.pk})

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete_account.html'
    success_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user == self.get_object()

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user.profile_picture:
            user.profile_picture.delete()
        return super().delete(request, *args, **kwargs)

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = CombinedProfileForm
    template_name = 'users/edit_profile.html'
    
    def get_object(self):
        return self.request.user.profile
    
    def form_valid(self, form):
        profile = form.save(commit=False)
        # Mise à jour des champs utilisateur
        user = profile.user
        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.save()
        profile.save()
        return redirect('users:profile', pk=self.request.user.pk)

class DeleteAccountView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:login')
    template_name = 'users/delete_account.html'
    
    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        logout(request)
        return super().delete(request, *args, **kwargs)
