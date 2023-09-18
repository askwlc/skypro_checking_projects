from django.shortcuts import render

from .models import EmailConfirmation


class EmailVerifiedRequiredMixin(object):
    """Миксин проверки верификации."""
    def dispatch(self, request, *args, **kwargs):
        email_confirmation_exists = EmailConfirmation.objects.filter(
            user=request.user, confirmed=True
        ).exists()
        if not email_confirmation_exists:
            return render(request, 'email/email_verification_required.html')
        return super().dispatch(request, *args, **kwargs)
