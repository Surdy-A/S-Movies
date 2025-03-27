from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

# class CustomUserCreationForm(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     email = forms.EmailField(required=True)
#     image = forms.ImageField(required=False)

#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'image']

# class LoginForm(AuthenticationForm):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

# class SignUpForm(forms.ModelForm):
#     class Meta:
#         model = User  # Link to the User model
#         fields = ["firstName", "lastName", "username", "email", "password", "agree", "image"]  # Match your model's fields
#         labels = {
#             "firstName": "First Name",
#             "lastName": "Last Name",
#             "username": "Username",
#             "email": "Email Address",
#             "password": "Password",
#             "agree": "I agree to the Privacy Policy",
#             "image": "Profile Image",
#         }
#         widgets = {
#             "firstName": forms.TextInput(attrs={"class": "sign__input", "placeholder": "Enter your first name"}),
#             "lastName": forms.TextInput(attrs={"class": "sign__input", "placeholder": "Enter your last name"}),
#             "username": forms.TextInput(attrs={"class": "sign__input", "placeholder": "Choose a username"}),
#             "email": forms.EmailInput(attrs={"class": "sign__input", "placeholder": "Enter your email address"}),
#             "password": forms.PasswordInput(attrs={"class": "sign__input", "placeholder": "Enter your password"}),
#             "agree": forms.CheckboxInput(attrs={"class": "sign__input", "id": "remember"}),
#             "image": forms.ClearableFileInput(attrs={"class": "sign__input"}),
#         }


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'sign__input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'sign__input', 'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'sign__input', 'placeholder': 'User Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'sign__input', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'sign__input', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'sign__input', 'placeholder': 'Confirm Password'}))
    agree = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'checked': 'checked'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'agree']
