from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User,Role


# =========================
# ADMIN FORMS (REQUIRED)
# =========================

class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'status')


class UserAdminChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


# =========================
# PUBLIC REGISTRATION FORM
# =========================

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'phone_number', 'status', 'role']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Username'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number'
            }),
        
            'status': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }


# =========================
# ROLE FORM
# =========================

class RoleForm(forms.ModelForm):
     class Meta:
         model = Role
         fields = ['role_name', 'description']

         widgets = {
             'role_name': forms.TextInput(attrs={
                 'class': 'form-control',
                 'placeholder': 'Enter role name'
             }),
             'description': forms.Textarea(attrs={
                 'class': 'form-control',
                 'placeholder': 'Enter description',
                 'rows': 3
             }),
         }
