from django.urls import path
from .views import register, user_login, profile, user_logout
from django.contrib.auth import views as auth_views
from django.urls.base import reverse_lazy

app_name = 'users'

urlpatterns = [
    path("register/", register, name="register"),
     path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("profile/", profile, name="profile"),

    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="auth/password_reset_form.html"), name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name="auth/password_reset_form.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="auth/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="auth/password_reset_form.html"), name="password_reset_complete")
]
