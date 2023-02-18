from django.views.generic import TemplateView
from rest_framework import viewsets

from neonlush.apps.main.api.serializers import NotifyMeSerializer
from neonlush.apps.main.models import NotifyMe


# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class NotifyMeApiViewSet(viewsets.ModelViewSet):
    queryset = NotifyMe.objects.all()
    serializer_class = NotifyMeSerializer
