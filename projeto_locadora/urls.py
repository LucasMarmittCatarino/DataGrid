from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/login/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('locadora/', include('locadora.urls')),
    path('contato/', include('contato.urls')),   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

