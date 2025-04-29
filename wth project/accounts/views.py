from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import CreateView, UpdateView, TemplateView, FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy
from .models import User
from .forms import RegisterForm, LoginForm, ProfileForm

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return response

class LoginView(AuthLoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('profile')

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class EditProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class LogoutConfirmView(TemplateView):
    template_name = 'accounts/logout_confirm.html'

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')