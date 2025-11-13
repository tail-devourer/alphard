from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('sign-in', views.SignInView.as_view(), name='sign_in'),
    path('get-started', views.GetStartedView.as_view(), name='get_started'),
]
