from django.views import View
from django.utils import timezone
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from .mixins import AccountActionEmailDispatcher
from .forms import CustomUserCreationForm

User = get_user_model()


class SignInView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, 'sign-in.html', {
            'form': AuthenticationForm(request),
        })

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

        return render(request, 'sign-in.html', {
            'form': form,
        })


class GetStartedView(View, AccountActionEmailDispatcher):
    email_reverse = 'confirm_email'
    email_subject = 'Confirm your email'
    email_template = 'email/confirm-email.txt'
    email_html_template = 'email/confirm-email.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, 'get-started.html', {
            'form': CustomUserCreationForm(),
        })

    def post(self, request):
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            self.send_mail(
                request=request,
                user=user,
            )

            return redirect('home')

        return render(request, 'get-started.html', {
            'form': form,
        })


class ConfirmEmailView(View):

    def get(self, request, uid, token):
        try:
            pk = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=pk)

            if not default_token_generator.check_token(user, token):
                raise ValueError
        except (ValueError, User.DoesNotExist):
            return render(request, 'invalid-request.html', {})

        if not user.email_verified_at:
            user.email_verified_at = timezone.now()
            user.save()

        return redirect('home')
