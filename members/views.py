from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy, reverse
from .forms import SignUpFrom, EditProfileForm, PasswordChangingForm
from blog.models import Profile, Post, User


class ShowProfileView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'
    ordering = ['-date_time']
    
    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfileView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        user_posts = Post.objects.filter().order_by('-date_time')
        context['page_user'] = page_user
        context['user_posts'] = user_posts
        return context


class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    fields = ['bio','profile_pic']
    success_url = reverse_lazy('home')
        
        
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')
    
    
def password_success(request):
    return render(request, 'registration/password_success.html')


class UserRegisterView(generic.CreateView):
    form_class = SignUpFrom
    template_name = 'registration/register.html'    
    success_url = reverse_lazy('login')
    
    
class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')
    
    def get_object(self):
        return self.request.user