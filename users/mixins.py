from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import Http404
from django.contrib.auth import get_user_model
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


# Local Imports
from . import forms


User = get_user_model()


class UserPassesHimselfMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Test if the User who Sent the Reqeust he is the Logged in User"""

    def test_func(self):
        return self.request.user == self.get_object()

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        qs = User.objects.filter(username=username)
        if qs.exists():
            return qs.first()
        else:
            raise Http404("User Not Found")


class VerifyUserIdentity(UserPassesHimselfMixin, FormView):
    """Verify User Identity By Form and Redirect to another Page
    - provide Form that has ```verify()``` mehtod that return bool value
    - else Raise attribute error
    - Provide Success URL"""

    template_name = "users/verify_identity.html"
    form_class = forms.VerifyUserIdentityForm
    success_url = None
    if_verified_msg = "Your Identity is Verified Successfully"
    not_verified_msg = "Your Identity is not Verified"
    invalid_form_message = "Please Enter Right Data"
    context_object_name = "form"


    def check_form_valid(self, form):
        """Check if the Form is has verfiy() method"""
        if not hasattr(form, "verify"):
            raise AttributeError("Form Class must have a verify() method")

    def form_valid(self, form: forms.VerifyUserIdentityForm):
        """Verify User Identity and Redirect to another Page"""
        if self.check_form_valid(form):
            verified = form.verify()
            if verified:
                messages.success(self.request, self.if_verified_msg)
                return redirect(self.success_url)
            else:
                messages.error(self.request, self.not_verified_msg)
                return self.get(self.request)

    def form_invalid(self, form):
        messages.error(self.request, self.invalid_form_message)
        return self.get(self.request)
