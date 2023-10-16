from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('supporting_system.urls')),
    path('account/', include("django.contrib.auth.urls"))
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, docuent_root = settings.STATIC_ROOT)
