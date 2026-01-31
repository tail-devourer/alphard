from django.urls import path
from .views import (
    SignInView,
    GetStartedView,
)

urlpatterns = [
    path('sign-in', SignInView.as_view(), name='sign_in'),
    path('get-started', GetStartedView.as_view(), name='get_started'),
]
