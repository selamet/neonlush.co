from django.urls import path

from apps.user.api.v1.views import RegisterAPIView, LoginAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api_user_register'),
    path('login/', LoginAPIView.as_view(), name='api_user_login'),
]
