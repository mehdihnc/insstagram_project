from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import User
from .forms import UserRegistrationForm, UserUpdateForm

class UserRegistrationView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    fields = ['username', 'email', 'password']
    success_url = '/login/'

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = self.object.get_stats()
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/edit_profile.html'
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk}) 

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = '/'