from django.urls import path

from .views import UserRegistrationView, UserLoginView


urlpatterns = [
    path(
        "auth/register/",
        UserRegistrationView.as_view(),
        name="user_register_view",
    ),
    path(
        "auth/login/",
        UserLoginView.as_view(),
        name="user_login_view",
    ),
]
