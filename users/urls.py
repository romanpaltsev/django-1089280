from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='users:login'), name="logout"),

    path("password-change/", PasswordChangeView.as_view(), name="password_change"),
    path("password-change/done/", PasswordChangeDoneView.as_view(), name="password_change_done"),

    path("register/", views.RegisterUser.as_view(), name="register"),
    path("profile/", views.ProfileUser.as_view(), name="profile"),
]