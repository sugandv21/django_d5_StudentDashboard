from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentProfile


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Username"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter Password"})
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter Email"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Choose a Username"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter Password"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm Password"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            StudentProfile.objects.get_or_create(user=user)

        return user
