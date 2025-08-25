from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import StudentProfile
from .forms import RegisterForm
from .forms import LoginForm


def home(request):
    return render(request, "dashboard/layout/home.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  
            StudentProfile.objects.create(user=user)
            messages.success(request, "Registration successful. Please login.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, "dashboard/layout/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back {user.username}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "dashboard/layout/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


@login_required
def student_dashboard(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    return render(request, "dashboard/layout/dashboard.html", {"profile": profile})
