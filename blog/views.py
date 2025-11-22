from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import forms, login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .forms import CustomUserCreationForm, PasswordResetForm, PasswordResetConfirmForm
from .tasks import send_confirmation_email, send_password_reset_email


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
        confirmation_url = request.build_absolute_uri(
            reverse("confirm_user", kwargs={"uid": uid, "token": token})
        )

        send_confirmation_email.delay(user.full_name, user.email, confirmation_url)

        return render(request, "get-started-done.html", {
            "email": email,
        })

    def post(self, request):
        request.session.pop("confirmUser", None)
        return redirect("get_started")


class ConfirmUserView(View):

    def get(self, request, uid, token):
        request.session.pop("confirmUser", None)

        User = get_user_model()

        try:
            pk = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=pk)

            if user.is_active or not default_token_generator.check_token(user, token):
                raise ValueError
        except:
            return render(request, "confirm-user-fail.html", {})

        user.is_active = True
        user.save()

        return redirect("sign_in")


class PasswordResetView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")

        return render(request, "password-reset-request.html", {
            "form": PasswordResetForm(),
        })

    def post(self, request):
        form = PasswordResetForm(data=request.POST)

        if form.is_valid():
            request.session["email"] = form.cleaned_data["email"]
            return redirect("request_password_reset_done")

        return render(request, "password-reset-request.html", {
            "form": form,
        })


class PasswordResetDoneView(View):

    def get(self, request):
        email = request.session.get("email")

        if not email:
            return redirect("request_password_reset")

        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect("request_password_reset")

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = request.build_absolute_uri(
            reverse("password_reset", kwargs={"uid": uid, "token": token})
        )

        send_password_reset_email.delay(user.full_name, user.email, reset_url)

        return render(request, "password-reset-request-done.html", {
            "email": email,
        })

    def post(self, request):
        request.session.pop("email", None)
        return redirect("request_password_reset")


class PasswordResetConfirmView(View):

    def get(self, request, uid, token):
        if request.user.is_authenticated:
            return redirect("home")

        User = get_user_model()

        try:
            pk = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=pk)

            if not default_token_generator.check_token(user, token):
                raise ValueError
        except:
            return render(request, "password-reset-fail.html", {})

        return render(request, "password-reset-confirm.html", {
            "form": PasswordResetConfirmForm(user=user),
        })

    def post(self, request, uid, token):
        request.session.pop("email", None)

        User = get_user_model()

        try:
            pk = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=pk)

            if not default_token_generator.check_token(user, token):
                raise ValueError
        except:
            return render(request, "password-reset-fail.html", {})

        form = PasswordResetConfirmForm(user=user, data=request.POST)

        if form.is_valid():
            user.set_password(form.cleaned_data["password1"])
            user.save()

            return redirect("sign_in")

        return render(request, "password-reset-confirm.html", {
            "form": form,
        })


class LogoutView(View):

    def post(self, request):
        logout(request)
        return redirect("home")


class ProfileView(View):

    def get(self, request, username):
        User = get_user_model()
        user = get_object_or_404(User, username=username)

        return render(request, "profile.html", {
            "user": user,
        })
