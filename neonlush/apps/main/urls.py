from django.urls import path

from neonlush.apps.main.views import HomeView

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
