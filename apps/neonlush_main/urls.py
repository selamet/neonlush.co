from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/test-get/', views.test_get, name='test_get'),
    path('api/test-post/', views.test_post, name='test_post'),
]
