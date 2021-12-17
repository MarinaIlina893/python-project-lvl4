from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class MessageMixin:
    """
    Add a message on form submission.
    """
    success_message = _("ОК")
    error_message = _("Something went wrong")

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, self.error_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data
        )
