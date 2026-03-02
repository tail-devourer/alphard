from django.urls import path
from .views import (
    SignInView,
    GetStartedView,
    ForgotPasswordView,
    ConfirmEmailView,
    ProfileView,
)

urlpatterns = [
    path('sign-in', SignInView.as_view(), name='sign_in'),
    path('get-started', GetStartedView.as_view(), name='get_started'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot_password'),
    path('confirm-email/<uid>/<token>', ConfirmEmailView.as_view(), name='confirm_email'),
    path('u/<username>', ProfileView.as_view(), name='profile'),
]
