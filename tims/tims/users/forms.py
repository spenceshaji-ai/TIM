from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import User,Role
from django import forms
from django.contrib.auth.forms import UserCreationForm


from django import forms
from django.contrib.auth.forms import  UserChangeForm



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


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """

"""class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone', 'role', 'status']

        widgets = {
            'password': forms.PasswordInput(),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }"""



class RegisterForm(UserCreationForm):
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        empty_label="Select Role"
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone_number',
            'role',
            'status'
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )

    
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
