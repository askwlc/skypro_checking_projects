from django.http import HttpResponseForbidden
from .models import EmailConfirmation


class EmailVerifiedRequiredMixin(object):
    """Миксин проверки верификации."""
    def dispatch(self, request, *args, **kwargs):
        email_confirmation_exists = EmailConfirmation.objects.filter(user=request.user, confirmed=True).exists()
        if not email_confirmation_exists:
            return HttpResponseForbidden("Нужно верифицировать почту для доступа к этой странице.")
        return super().dispatch(request, *args, **kwargs)
