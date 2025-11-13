from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import forms, login


class HomeView(View):

    def get(self, request):
        return render(request, "home.html", {})


class SignInView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")

        return render(request, "sign-in.html", {
            "form": forms.AuthenticationForm(request),
        })

    def post(self, request):
        form = forms.AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")

        return render(request, "sign-in.html", {
            "form": form,
        })


class GetStartedView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")

        return render(request, "get-started.html", {})
