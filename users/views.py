from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileForm, CustomUserRegistrationForm, LoginForm
from django.http import JsonResponse
from common.models import Position
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _
from django import forms

def view_profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def get_positions(request, department_id):
    positions = Position.objects.filter(department_id=department_id, is_deleted=False).values('id', 'name')
    return JsonResponse(list(positions), safe=False)

def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Hoşgeldin " + username + ", Başarıyla giriş yaptınız!")
                return redirect('home')
            else:
                error_message = "Kullanıcı adı veya şifre hatalı!"
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error_message': error_message})

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        UserModel = get_user_model()
        if not UserModel.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("Bu e-posta adresiyle kayıtlı bir kullanıcı bulunamadı.")
        return email

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm

class CustomSetPasswordForm(SetPasswordForm):
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        user = self.user
        # Son 3 şifreyi kontrol et
        last_passwords = user.password_history.order_by('-created_at')[:3] if hasattr(user, 'password_history') else []
        for old in last_passwords:
            if check_password(password1, old.password):
                raise forms.ValidationError(_('Yeni şifreniz, son üç şifrenizle aynı olamaz.'))
        return password1

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm