from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import forms, login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .forms import CustomUserCreationForm
from .tasks import send_confirmation_email


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

        return render(request, "get-started.html", {
            "form": CustomUserCreationForm(),
        })

    def post(self, request):
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            request.session["confirmUser"] = user.email

            return redirect("get_started_done")

        return render(request, "get-started.html", {
            "form": form,
        })


class GetStartedDoneView(View):

    def get(self, request):
        email = request.session.get("confirmUser")

        if not email:
            return redirect("get_started")

        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect("get_started")

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        confirmation_url = request.build_absolute_uri(f"/confirm-user/{uid}/{token}")

        send_confirmation_email.delay(user.full_name, user.email, confirmation_url)

        return render(request, "get-started-done.html", {
            "email": email
        })

    def post(self, request):
        request.session.pop("confirmUser")
        return redirect("get_started")


class LogoutView(View):

    def post(self, request):
        logout(request)
        return redirect("home")
