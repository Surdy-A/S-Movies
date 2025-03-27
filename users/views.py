from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password  # Secure password storage
from django.contrib import messages

# def register(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("profile")
#     else:
#         form = CustomUserCreationForm()
#     return render(request, "auth/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
    else:
        form = LoginForm()
    return render(request, "auth/login.html", {"form": form})

@login_required
def profile(request):
    return render(request, "auth/profile.html")

def user_logout(request):
    logout(request)
    return redirect("login")

# def register(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Handle the form data (e.g., save user)
#             user = form.save(commit=False)  # Don't save yet
#             user.password = make_password(user.password)  # Hash the password
#             user.save()  # Now save the user
#             print("Form Data:", form.cleaned_data)
#             print("FirstName:", form.cleaned_data["firstName"])
#             return redirect("/movies")  # Change 'home' to your success URL
#     else:
#         form = SignUpForm()
    
#     return render(request, "auth/register.html", {"form": form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            print("Form Data:", form.cleaned_data)
            return redirect('/movies')
    else:
        form = UserRegistrationForm()


    return render(request, 'auth/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('/movies')  # Redirect to movies page after login
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, "auth/login.html")

