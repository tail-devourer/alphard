from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
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


class GetStartedView(View):

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
            return redirect('home')

        return render(request, 'get-started.html', {
            'form': form,
        })
