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
from django.contrib.auth.forms import AuthenticationForm



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
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        help_text=""   # ❌ removes rules
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        help_text=""   # ❌ removes rules
    )
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
def clean_password1(self):
    password = self.cleaned_data.get("password1")

    from django.contrib.auth.password_validation import validate_password
    from django.core.exceptions import ValidationError

    try:
       validate_password(password)
    except ValidationError as e:
            # Show rules ONLY when invalid
        self.fields['password1'].help_text = "<br>".join(e.messages)
        raise forms.ValidationError(e.messages)

    return password


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

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Username"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password"
        })
    )