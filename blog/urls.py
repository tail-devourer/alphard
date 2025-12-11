from django.urls import path
from .views import auth, user, blog

urlpatterns = [
    # Blog
    path('', blog.HomeView.as_view(), name='home'),

    # Auth
    path('sign-in', auth.SignInView.as_view(), name='sign_in'),
    path('logout', auth.LogoutView.as_view(), name='logout'),
    path('get-started', auth.GetStartedView.as_view(), name='get_started'),
    path('get-started/done', auth.GetStartedDoneView.as_view(), name='get_started_done'),
    path('confirm-user/<uid>/<token>', auth.ConfirmUserView.as_view(), name='confirm_user'),
    path('reset/request', auth.PasswordResetView.as_view(), name='request_password_reset'),
    path('reset/request/done', auth.PasswordResetDoneView.as_view(), name='request_password_reset_done'),
    path('reset/<uid>/<token>', auth.PasswordResetConfirmView.as_view(), name='password_reset'),

    # User
    path('u/<username>', user.ProfileView.as_view(), name='profile'),
    path('user/settings', user.SettingsView.as_view(), name='user_settings')
]
