from django.views import View
from django.shortcuts import render


class HomeView(View):

    def get(self, request):
        return render(request, "home.html", {})


class SignInView(View):

    def get(self, request):
        return render(request, "sign-in.html", {})


class GetStartedView(View):

    def get(self, request):
        return render(request, "get-started.html", {})
