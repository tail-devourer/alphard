from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()


class GetStartedView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")

        return render(request, "get-started.html", {})
