from django.views import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms import PersonalInfoUpdateForm
from ..tasks import send_mail

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
        old_email = request.user.email
        old_username = request.user.username

        form = PersonalInfoUpdateForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user,
        )

        if form.is_valid():
            context = {
                "full_name": form.cleaned_data["full_name"],
            }

            new_username = form.cleaned_data["username"]
            new_email = form.cleaned_data["email"]

            email_changed = old_email != new_email
            username_changed = old_username != new_username

            if email_changed:
                context["new_email"] = new_email

            if username_changed:
                context["old_username"] = old_username
                context["new_username"] = new_username

            if email_changed or username_changed:
                send_mail.delay(
                    to=[old_email],
                    subject="Account Details Updated",
                    template_name="email/account-update.txt",
                    html_template_name="email/account-update.html",
                    context=context,
                )

            form.save()
            request.user.refresh_from_db()

        return render(request, "settings.html", {
            "form": form,
        })
