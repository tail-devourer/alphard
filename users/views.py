from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .mixins import AccountActionEmailDispatcher
from .forms import CustomUserCreationForm


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
    pass
