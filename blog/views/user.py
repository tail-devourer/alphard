from django.views import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model


class ProfileView(View):

    def get(self, request, username):
        User = get_user_model()
        user = get_object_or_404(User, username=username)

        return render(request, "profile.html", {
            "user": user,
        })
