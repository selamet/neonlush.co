from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from neonlush import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('neonlush.apps.main.urls')),
    path('user/', include('neonlush.apps.user.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
