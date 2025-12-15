from django.views import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms import PersonalInfoUpdateForm

User = get_user_model()

class ProfileView(View):

    def get(self, request, username):
        user = get_object_or_404(User, username=username)

        return render(request, "profile.html", {
            "user": user,
        })


class SettingsView(LoginRequiredMixin, View):
    login_url = "home"
    redirect_field_name = None

    def get(self, request):
        return render(request, "settings.html", {
            "form": PersonalInfoUpdateForm(instance=request.user),
        })

    def post(self, request):
        form = PersonalInfoUpdateForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user,
        )

        if form.is_valid():
            form.save()
            request.user.refresh_from_db()

        return render(request, "settings.html", {
            "form": form,
        })
