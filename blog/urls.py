from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('sign-in', views.SignInView.as_view(), name='sign_in'),
    path('get-started', views.GetStartedView.as_view(), name='get_started'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('get-started/done', views.GetStartedDoneView.as_view(), name='get_started_done'),
    path('confirm-user/<uid>/<token>', views.ConfirmUserView.as_view(), name='confirm_user'),
    path('u/<username>', views.ProfileView.as_view(), name='profile'),
    path('reset/request', views.PasswordResetView.as_view(), name='request_password_reset'),
    path('reset/request/done', views.PasswordResetDoneView.as_view(), name='request_password_reset_done'),
    path('reset/<uid>/<token>', views.PasswordResetConfirmView.as_view(), name='password_reset'),
]
