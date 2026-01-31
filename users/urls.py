from django.urls import path
from .views import (
    GetStartedView,
)

urlpatterns = [
    path('get-started', GetStartedView.as_view(), name='get_started'),
]
