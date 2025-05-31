from django import forms
from .models import Profile
from django.contrib.auth.models import User
from common.models import Department, Position

#Profil Formu
class ProfileForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_deleted=False),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.filter(is_deleted=False),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Profile
        fields = ['firstname', 'lastname', 'birth_date', 'phone', 'email', 'image', 'position', 'department']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.department:
            self.fields['position'].queryset = Position.objects.filter(
                department=self.instance.department,
                is_deleted=False
            )
        if self.instance and self.instance.birth_date:
            self.initial['birth_date'] = self.instance.birth_date.strftime('%Y-%m-%d')


# Kullanıcı Kayıt Formu
class CustomUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Şifreler Uyuşmuyor!!')
        return cd['password2']

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kullanıcı Adı'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Şifre'
        })
    )