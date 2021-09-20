from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from project.settings.base import MEDIA_URL, MEDIA_ROOT
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('monopoly/', include('monopoly.urls')),
    path('api/', include('monopoly.api.urls')),
    # API PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
