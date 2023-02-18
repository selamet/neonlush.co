from django.urls import path
from rest_framework.routers import DefaultRouter

from neonlush.apps.main.views import HomeView, NotifyMeApiViewSet

app_name = 'main'

router = DefaultRouter()
router.register('notify-me', NotifyMeApiViewSet, basename='notify-me')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
urlpatterns += router.urls
