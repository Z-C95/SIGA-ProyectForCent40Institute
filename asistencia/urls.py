from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from asistencias import views as av

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', av.home, name='home'),
    path('app/', include(('asistencias.urls', 'asistencias'), namespace='asistencias')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
