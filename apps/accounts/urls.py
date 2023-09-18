from django.urls import path

from .views import (CustomLoginView, CustomLogoutView, confirm_email, register,
                    resend_verification_email)

urlpatterns = [
    path('register/', register, name='register'),
    path('', CustomLoginView.as_view(), name='login'),
    path('confirm-email/<str:confirmation_code>/', confirm_email,
         name='confirm_email'),
    path('resend_verification/', resend_verification_email,
         name='resend_verification'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
